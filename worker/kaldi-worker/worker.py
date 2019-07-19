#!/usr/bin/python
from connector import *
import os
import shutil

import subprocess
from minio_communication import download_from_bucket, upload_to_bucket
import JSON

script_root_path = os.path.dirname(os.path.realpath(__file__))
workspace_path = os.path.join(script_root_path, 'workspace')
base_model_path = os.path.join(workspace_path, 'base-model.zip')

lexicon_path = os.path.join(workspace_path, 'lexicon.txt')
corpus_path = os.path.join(workspace_path, 'corpus.txt')
if __name__ == "__main__":
    try:
        conf, tasks, status, minio = parse_args(
            'Kaldi Worker Connector', task_queue='Kaldi-Queue')

        for task in tasks.listen():
            print("Read task from queue:")
            print(task)
            
            os.makedirs(workspace_path)

            # TODO: load base model from minio
            download_from_bucket(minio_client, bucket_in, lexicon, "/data_prep_worker/in/")
            # TODO: load resources
            # TODO: train resources
            subprocess.call("create_new_graph.sh"+ " {} {}".format(lexicon_path,corpus_path),shell=True)
            # TODO: unload resources


            shutil.rmtree(workspace_path)

            # write in status queue
            status.submit(KaldiStatus(id=KaldiStatusCode.SUCCESS))

    except KeyboardInterrupt:
        pass
