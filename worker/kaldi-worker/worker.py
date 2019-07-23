#!/usr/bin/python
from connector import *
import os
import shutil

import subprocess
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets
import redis_config
import json

acoustic_model_bucket = minio_buckets['ACOUSTIC_MODELS_BUCKET']
project_bucket = minio_buckets["PROJECT_BUCKET"]

script_root_path = os.path.dirname(os.path.realpath(__file__))
workspace_path = os.path.join(script_root_path, 'workspace')
base_model_path = os.path.join(workspace_path, 'base-model.zip')

lexicon_path = os.path.join(workspace_path, 'lexicon.txt')
corpus_path = os.path.join(workspace_path, 'corpus.txt')
acoustic_model_folder = os.path.join(script_root_path,"acc_models")

new_graph_dir = os.path.join(script_root_path,"new_graph")
new_graph_archive = os.path.join(script_root_path,"graph")
archive_format ="zip"

downloaded_acoustic_models = set()
if not os.path.exists(acoustic_model_folder):
    os.makedirs(acoustic_model_folder)
if __name__ == "__main__":
    try:
        conf, tasks, status, minio_client = parse_args('Kaldi Worker Connector', task_queue=redis_config.redis_queues["KALDI_QUEUE"])

        for task in tasks.listen():
            print("Read task from queue:")
            print(task)

            acoustic_model_id = task["acoustic_model_id"]
            project_id = task["project_id"]

            if not os.path.exists(acoustic_model_folder):
                        os.makedirs(workspace_path)

            # cache models when used once and reduce download
            cur_acoustic_model_path = os.path.join(acoustic_model_folder,acoustic_model_id)
            if(acoustic_model_id not in downloaded_acoustic_models):
                os.makedirs(cur_acoustic_model_path)
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/final.mdl", os.path.join(cur_acoustic_model_path,"final.mdl"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/tree", os.path.join(cur_acoustic_model_path,"tree"))

                downloaded_acoustic_models.add(acoustic_model_id)
            

            # TODO: load resources
            download_from_bucket(minio_client, project_bucket, project_id + "/lexicon.txt", lexicon_path)
            download_from_bucket(minio_client, project_bucket, project_id + "/corpus.txt", corpus_path)
            # TODO: train resources
            os.chdir("/kaldi/scripts/")
            subprocess.call("/kaldi/scripts/create_new_graph.sh"+ " {} {} {} {} {}".format(lexicon_path,corpus_path,cur_acoustic_model_path,new_graph_dir,workspace_path),shell=True)
            os.chdir("/")
            # TODO Upload new model
            shutil.make_archive(new_graph_archive,archive_format,workspace_path,new_graph_dir)
            upload_to_bucket(minio_client,project_bucket,project_id + "/graph.zip", new_graph_archive + "." + archive_format)
            # TODO: unload resources
            shutil.rmtree(workspace_path)

            # write in status queue
            status.submit(KaldiStatus(id=KaldiStatusCode.SUCCESS))

    except KeyboardInterrupt:
        shutil.rmtree(acoustic_model_folder)
        shutil.rmtree(workspace_path)
        pass
