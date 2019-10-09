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

acoustic_model_folder = os.path.join(script_root_path,"acc_models")

downloaded_acoustic_models = set()
if os.path.exists(acoustic_model_folder):
    shutil.rmtree(acoustic_model_folder)
os.makedirs(acoustic_model_folder)


if os.path.exists(workspace_path):
    shutil.rmtree(workspace_path)


def finish_logging(log_file_handler, minio_client, task):
    log_file_handler.close()
    logfile_result = upload_to_bucket(minio_client, minio_buckets["LOG_BUCKET"], "decode_worker/{}/{}".format(task.training_id, "log.txt"), "/log.txt")
    if not logfile_result[0]:
        print("An error occurred during the upload of the logfile.")
    print("Logfile was successfully uploaded")


if __name__ == "__main__":
    try:
        conf, tasks, status, minio_client = parse_args('Decode Worker Connector', task_queue=redis_config.redis_queues["DECODING_QUEUE"])

        for task in tasks.listen():
            print("Received the following task from Decode-Queue:")
            print(task)

            task = DecodeTask(**task)

            acoustic_model_id = str(task["acoustic_model_id"])
            audioresource_uuids = task["audio_uuids"]
            training_id = str(task["training_id"])
            decode_uuid = task["decode_uuid"]

            log_file_handler = open("/log.txt", "w")
            log_file_handler.write("Starting to process the received task \n")
            log_file_handler.write("{}\n".format(task))

            if not os.path.exists(acoustic_model_folder):
                os.makedirs(workspace_path)
                log_file_handler.write("Needed acoustic model directory did not exist. Therefore, it was created! \n")
            log_file_handler.write("Needed acoustic model directory exists. Processing continues! \n")


            # cache acoustic models when used once and reduce download
            try:
                log_file_handler.write("Trying to download all needed acoustic model files! \n")
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
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to download all needed acoustic model files, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("At least one download failed! Therefore, the task failed too!\n")

                finish_logging(log_file_handler, minio_client, task)

                status.submit(DecodeStatus(id=DecodeStatusCode.FAILURE, decode_uuid=decode_uuid, transcripts=result))
            log_file_handler.write("Successfully downloaded all needed acoustic model files. Processing continues! \n")

            # Download Graph files from training
            try:
                log_file_handler.write("Trying to download graph archive which is needed for decoding! \n")
                cur_graph_path = os.path.join(workspace_path,"graph")
                download_graph_path = os.path.join(workspace_path, "graph.zip")
                download_from_bucket(minio_client, training_bucket, training_id + "/graph.zip", download_graph_path)
                shutil.unpack_archive(download_graph_path, cur_graph_path)
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to download the graph archive, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to download the needed graph archive. Therefore, the task failed!\n")

                finish_logging(log_file_handler, minio_client, task)

                status.submit(DecodeStatus(id=DecodeStatusCode.FAILURE, decode_uuid=decode_uuid, transcripts=result))
            log_file_handler.write("Successfully downloaded graph archive. Processing continues! \n")


            # Download wav files to decode
            try:
                log_file_handler.write("Trying to download all audio files which need to be decoded! \n")
                for uuid in audioresource_uuids:
                    download_from_bucket(minio_client, decode_bucket, str(uuid) , os.path.join(workspace_path, str(uuid) + ".wav"))
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to download all needed audio files, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("At least one download failed. Therefore, this task failed too! \n")

                finish_logging(log_file_handler, minio_client, task)

                status.submit(DecodeStatus(id=DecodeStatusCode.FAILURE, decode_uuid=decode_uuid, transcripts=result))
            log_file_handler.write("Successfully downloaded all audio files. Processing continues! \n")

            # create data dir
            try:
                log_file_handler.write("Trying to create utt2spk and wav.scp files for the decode task! \n")
                data_path = os.path.join(workspace_path,"data")
                os.makedirs(data_path)
                with open(os.path.join(data_path,"utt2spk"),"w") as f:
                    for i,uuid in enumerate(audioresource_uuids):
                        f.write("{} generic_speaker{}".format(uuid,i))

                with open(os.path.join(data_path,"wav.scp"),"w") as f:
                    for uuid in audioresource_uuids:
                        f.write("{} {}".format(uuid,os.path.join(workspace_path, str(uuid) + ".wav")))
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to create the utt2spk and wav.scp files, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("At least one file was not created!\n")

                finish_logging(log_file_handler, minio_client, task)

                status.submit(DecodeStatus(id=DecodeStatusCode.FAILURE, decode_uuid=decode_uuid, transcripts=result))
            log_file_handler.write("Successfully created utt2spk and wav.scp files! Processing continues! \n")

            # decode
            try:
                log_file_handler.write("Decoding of the downloaded audio files starts! \n")
                os.chdir("/kaldi/scripts/")
                subprocess.call("/kaldi/scripts/decode.sh"+ " {} {} {}".format(workspace_path, cur_acoustic_model_path, cur_graph_path),shell=True)
                os.chdir("/")
                decode_path = os.path.join(cur_acoustic_model_path,"decode")
            except Exception as e:
                print(e)
                log_file_handler.write("During the decoding process an error has occurred which leads to a failing task! \n")

                finish_logging(log_file_handler, minio_client, task)

                status.submit(DecodeStatus(id=DecodeStatusCode.FAILURE, decode_uuid=decode_uuid, transcripts=result))
            log_file_handler.write("Successfully decoded all audio files! \n")

            try:
                log_file_handler.write("Final step: Retrieve decoding transcripts! \n")
                result = dict()
                # extract from acoustic_model/decode
                with open(os.path.join(decode_path, "log", "decode.1.log")) as f:
                    for line in f:
                        line = line.split()
                        if line[0] in audioresource_uuids:
                            result[line[0]]=[" ".join(line[1:])]

                print("FOUND RESULTS:\n"+str(result))
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to retrieve the decoding transcript, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to access the requested file, or no transcript was found! \n")

                finish_logging(log_file_handler, minio_client, task)

                status.submit(DecodeStatus(id=DecodeStatusCode.FAILURE, decode_uuid=decode_uuid, transcripts=result))
            log_file_handler.write("Successfully retrieved the decoding transcripts!\n")

            finish_logging(log_file_handler, minio_client, task)

            # unload resources
            shutil.rmtree(workspace_path)
            shutil.rmtree(decode_path)

            status.submit(DecodeStatus(id=DecodeStatusCode.SUCCESS, decode_uuid=decode_uuid, transcripts=result))

    except KeyboardInterrupt:
        #cleanup
        shutil.rmtree(acoustic_model_folder)
        shutil.rmtree(workspace_path)
        pass
