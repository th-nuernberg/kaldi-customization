#!/usr/bin/python
from connector import *
import os
import shutil

import subprocess
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
import redis_config
import json

acoustic_model_bucket = minio_buckets['ACOUSTIC_MODELS_BUCKET']
training_bucket = minio_buckets["TRAINING_BUCKET"]

script_root_path = os.path.dirname(os.path.realpath(__file__))
workspace_path = os.path.join(script_root_path, 'workspace')
base_model_path = os.path.join(workspace_path, 'base-model.zip')

lexicon_path = os.path.join(workspace_path, 'lexicon.txt')
corpus_path = os.path.join(workspace_path, 'corpus.txt')
acoustic_model_folder = os.path.join(script_root_path,"acc_models")

downloaded_acoustic_models = set()
if os.path.exists(acoustic_model_folder):
    shutil.rmtree(acoustic_model_folder)
os.makedirs(acoustic_model_folder)

if __name__ == "__main__":
    try:
        conf, tasks, status, minio_client = parse_args('Kaldi Worker Connector', task_queue=redis_config.redis_queues["KALDI_QUEUE"])

        for task in tasks.listen():
            print("Read task from queue:")
            print(task)

            acoustic_model_id = str(task["acoustic_model_id"])
            training_id = str(task["training_id"])

            if not os.path.exists(acoustic_model_folder):
                        os.makedirs(workspace_path)

            # cache models when used once and reduce download
            cur_acoustic_model_path = os.path.join(acoustic_model_folder,str(acoustic_model_id))
            phone_symbol_table = os.path.join(cur_acoustic_model_path,"phones.txt")
            if(acoustic_model_id not in downloaded_acoustic_models):
                os.makedirs(cur_acoustic_model_path)
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/final.mdl", os.path.join(cur_acoustic_model_path,"final.mdl"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/tree", os.path.join(cur_acoustic_model_path,"tree"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/phones.txt", phone_symbol_table)

                downloaded_acoustic_models.add(acoustic_model_id)
            

            # load resources
            download_from_bucket(minio_client, training_bucket, training_id + "/lexicon.txt", lexicon_path)
            download_from_bucket(minio_client, training_bucket, training_id + "/corpus.txt", corpus_path)

            # train resources
            new_graph_dir = os.path.join(script_root_path,"new_graph")
            os.chdir("/kaldi/scripts/")
            subprocess.call("/kaldi/scripts/create_new_graph.sh"+ " {} {} {} {} {} {}".format(lexicon_path,corpus_path,cur_acoustic_model_path,new_graph_dir,workspace_path,phone_symbol_table),shell=True)
            os.chdir("/")

            # Upload new model
            new_graph_archive = os.path.join(script_root_path,"graph")
            archive_format ="zip"
            shutil.make_archive(base_name=new_graph_archive, format=archive_format, root_dir=new_graph_dir, base_dir="./")
            upload_to_bucket(minio_client,training_bucket,training_id + "/graph.zip", new_graph_archive + "." + archive_format)

            # unload resources
            shutil.rmtree(workspace_path)

            # write in status queue
            status.submit(KaldiStatus(id=KaldiStatusCode.SUCCESS))

    except KeyboardInterrupt:
        shutil.rmtree(acoustic_model_folder)
        shutil.rmtree(workspace_path)
        pass
