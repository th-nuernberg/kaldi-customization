#!/usr/bin/python
from connector import *
import os
import shutil

import subprocess
from minio_communication import download_from_bucket, upload_to_bucket
import redis_config
import json

print("starting")

#def report_status_to_API(queue_status, status_queue, filename=None, message=None):
    '''
    By calling this function the status queue is updated.
    Possible updates for the status queue are:
        - InProgress --> queue_status = 21
        - Success    --> queue_status = 200
        - Failure    --> queue_status = 22
    As soon as the Data-Preparation-Worker receives a new task, its entry
    within the Status-Queue is updated to: In-Progress.
    Depending on the processing result, the status of the task can change into:
        - Success
        - Failure
    if queue_status == 21 and not message:
        message = "Task in progress"
    elif queue_status == 22 and not message:
        message == "Task has failed"
    elif queue_status == 200 and not message:
        message = "Task finished successfully"

    status_queue.submit({"type": "text-prep", "text": filename, "status": queue_status, "msg": message})
'''

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
os.makedirs(acoustic_model_folder)
if __name__ == "__main__":
    try:
        conf, tasks, status, minio_client = parse_args('Kaldi Worker Connector', task_queue=redis_config.redis_queues.KALDI_QUEUE)

        shutil.make_archive('/home/code/test_dicoms',
                    'zip',
                    '/home/code/',
                    'test_dicoms')

        for task in tasks.listen():
            print("Read task from queue:")
            print(task)
            task = json.loads(task[1])
            acoustic_model_bucket = task["acoustic-model_bucket"]
            acoustic_model_id = task["acoustic-model-id"]
            project_bucket = task["project-bucket"]
            project_uuid = task["project-uuid"]

            os.makedirs(workspace_path)

            # cache models when used once and reduce download
            cur_acoustic_model_path = os.path.join(acoustic_model_folder,acoustic_model_id)
            if(acoustic_model_id not in downloaded_acoustic_models)
                os.makedirs(cur_acoustic_model_path)
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/final.mdl", os.path.join(cur_acoustic_model_path,"final.mdl"))
                download_from_bucket(minio_client, acoustic_model_bucket, acoustic_model_id + "/tree", os.path.join(cur_acoustic_model_path,"tree"))

                downloaded_acoustic_models.add(acoustic_model_id)
            # TODO: load resources
            download_from_bucket(minio_client, project_bucket, project_uuid + "/lexicon.txt", lexicon_path)
            download_from_bucket(minio_client, project_bucket, project_uuid + "/corpus.txt", corpus_path)
            # TODO: train resources
            subprocess.call("scripts/create_new_graph.sh"+ " {} {} {} {} {}".format(lexicon_path,corpus_path,cur_acoustic_model_path,new_graph_dir,workspace_path),shell=True)
            # TODO Upload new model
            shutil.make_archive(new_graph_archive,archive_format,workspace_path,new_graph_dir)
            upload_to_bucket(minio_client,project_bucket,project_uuid + "/graph.zip", new_graph_archive)
            # TODO: unload resources
            shutil.rmtree(workspace_path)

            # write in status queue
            status.submit(KaldiStatus(id=KaldiStatusCode.SUCCESS))

    except KeyboardInterrupt:
        pass
