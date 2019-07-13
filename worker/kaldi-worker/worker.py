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
            task = KaldiTask(**task)
            print(task)

            os.makedirs(workspace_path)

            # TODO: load base model from minio
            # TODO: load resources
            # TODO: train resources
            # TODO: unload resources

            shutil.rmtree(workspace_path)

            # write in status queue
            status.submit(KaldiStatus(id=KaldiStatusCode.SUCCESS))

    except KeyboardInterrupt:
        pass
