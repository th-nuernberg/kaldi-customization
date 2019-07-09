#!/usr/bin/python
from connector import *
import os
import shutil

script_root_path = os.path.dirname(os.path.realpath(__file__))
workspace_path = os.path.join(script_root_path, 'workspace')
base_model_path = os.path.join(workspace_path, 'base-model.zip')


if __name__ == "__main__":
    try:
        conf, tasks, status, minio = parse_args(
            'Kaldi Worker Connector', task_queue='Kaldi-Queue')

        for task in tasks.listen():
            task = KaldiTask.fromJSON(task)
            print(task)

            os.makedirs(workspace_path)

            # load base model from minio
            minio.fget_object(
                task.base_bucket, task.base_object, base_model_path)

            # TODO: load resources
            # TODO: train resources

            # put target model to minio
            minio.fput_object(
                task.target_bucket, task.target_object, base_model_path)

            shutil.rmtree(workspace_path)

            # TODO: process task
            status.submit({'test': 'MyTestStatus'})

    except KeyboardInterrupt:
        pass
