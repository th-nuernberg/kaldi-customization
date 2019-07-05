#!/usr/bin/python

import json

from util import logger, logging, parse_args, TaskQueue


if __name__ == "__main__":
    try:
        conf, tasks, status, minio_client = parse_args(
            'Kaldi Worker Connector', task_queue='ASR-Queue')

        logger.debug(conf)

        for task in tasks:
            print(task)
            # TODO: process task
            status.submit({'test': 'MyTestStatus'})

    except KeyboardInterrupt:
        pass
