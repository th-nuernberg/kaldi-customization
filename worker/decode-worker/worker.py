#!/usr/bin/python
from connector import *
import os
import shutil

import subprocess
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
import redis_config
import json

acoustic_model_bucket = minio_buckets['ACOUSTIC_MODELS_BUCKET']
decode_bucket = minio_buckets["DECODING_BUCKET"]
training_bucket = minio_buckets["TRAINING_BUCKET"]

script_root_path = os.path.dirname(os.path.realpath(__file__))
workspace_path = os.path.join(script_root_path, 'workspace')

wav_file_path = os.path.join(workspace_path, 'tmp.wav')

acoustic_model_folder = os.path.join(script_root_path,"acc_models")

downloaded_acoustic_models = set()
if os.path.exists(acoustic_model_folder):
    shutil.rmtree(acoustic_model_folder)
os.makedirs(acoustic_model_folder)


if os.path.exists(workspace_path):
    shutil.rmtree(workspace_path)

if __name__ == "__main__":
    try:
        conf, tasks, status, minio_client = parse_args('Decode Worker Connector', task_queue=redis_config.redis_queues["DECODING_QUEUE"])

        for task in tasks.listen():
            print("Read task from queue:")
            print(task)

            acoustic_model_id = str(task["acoustic_model_id"])
            decode_file = task["decode_file"]
            training_id = str(task["training_id"])

            if not os.path.exists(acoustic_model_folder):
                        os.makedirs(workspace_path)

            # cache acoustic models when used once and reduce download
            cur_acoustic_model_path = os.path.join(acoustic_model_folder,str(acoustic_model_id))
            ivector_extractor_path = os.path.join(cur_acoustic_model_path,"extractor")
            if(acoustic_model_id not in downloaded_acoustic_models):
                os.makedirs(cur_acoustic_model_path)
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/final.mdl", os.path.join(cur_acoustic_model_path,"final.mdl"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/tree", os.path.join(cur_acoustic_model_path,"tree"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/cmvn_opts", os.path.join(cur_acoustic_model_path,"cmvn_opts"))

                os.makedirs(ivector_extractor_path)
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/final.dubm", os.path.join(cur_acoustic_model_path,"extractor/final.dubm"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/final.ie", os.path.join(cur_acoustic_model_path,"extractor/final.ie"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/final.ie.id", os.path.join(cur_acoustic_model_path,"extractor/final.ie.id"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/final.mat", os.path.join(cur_acoustic_model_path,"extractor/final.mat"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/global_cmvn.stats", os.path.join(cur_acoustic_model_path,"extractor/global_cmvn.stats"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/online_cmvn.conf", os.path.join(cur_acoustic_model_path,"extractor/online_cmvn.conf"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/extractor/splice_opts", os.path.join(cur_acoustic_model_path,"extractor/splice_opts"))

                downloaded_acoustic_models.add(acoustic_model_id)
            
            # Download Graph files from training
            cur_graph_path = os.path.join(workspace_path,"graph")
            download_graph_path = os.path.join(workspace_path, "graph.zip")
            download_from_bucket(minio_client, training_bucket, training_id + "/graph.zip", download_graph_path)
            shutil.unpack_archive(download_graph_path, cur_graph_path)


            # Download wav file to decode
            download_from_bucket(minio_client, decode_bucket, decode_file , wav_file_path)

            # create data dir
            data_path = os.path.join(workspace_path,"data")
            os.makedirs(data_path)
            with open(os.path.join(data_path,"utt2spk"),"w") as f:
                f.write("generic generic_speaker")
            
            with open(os.path.join(data_path,"wav.scp"),"w") as f:
                f.write("generic " + wav_file_path)

            # decode
            os.chdir("/kaldi/scripts/")
            subprocess.call("/kaldi/scripts/decode.sh"+ " {} {} {}".format(workspace_path, cur_acoustic_model_path, cur_graph_path),shell=True)
            os.chdir("/")
            decode_path = os.path.join(cur_acoustic_model_path,"decode")

            result = "ERROR"
            # extract from acoustic_model/decode
            with open(os.path.join(decode_path, "log", "decode.1.log")) as f:
                for line in f:
                    line = line.split()
                    if line[0] == 'generic':
                        result = " ".join(line[1:])

            print("FOUND RESULT:\n"+result)

            # unload resources
            shutil.rmtree(workspace_path)
            shutil.rmtree(decode_path)

            status.submit(DecodeStatus(id=DecodeStatusCode.SUCCESS, decode_uuid=decode_file, transcripts=[result]))

    except KeyboardInterrupt:
        #cleanup
        shutil.rmtree(acoustic_model_folder)
        shutil.rmtree(workspace_path)
        pass
