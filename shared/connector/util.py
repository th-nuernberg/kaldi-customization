import argparse
import json
import logging
import minio
import redis
import sys


logger = logging.getLogger('connector')
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_args(name, task_queue=None,
               status_queue='Status-Queue', more_args=None):
    """Parses arguments from argv,
        lambda more_args(parser) can be used to extend the default args
    """
    parser = argparse.ArgumentParser(
        description='{} for Redis and MinIO.'.format(name),
        formatter_class=lambda prog:
            argparse.RawTextHelpFormatter(prog, width=99999))

    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='verbose output'
    )

    if more_args:
        more_args(parser)

    # Redis
    parser.add_argument(
        '--redis-host', default='localhost',
        help='host name/address of redis [default: localhost]')
    parser.add_argument(
        '--redis-port', type=int, default=6379,
        help='port of redis [default: 6379]')
    parser.add_argument(
        '--redis-db', type=int, default=0,
        help='database id of redis [default: 0]')
    parser.add_argument(
        '--redis-password', default=None,
        help='password of the redis server')

    if task_queue:
        parser.add_argument(
            '--redis-task-queue', default=task_queue,
            help='key: list of tasks [default: {}]'.format(task_queue))

    parser.add_argument(
        '--redis-status-queue', default=status_queue,
        help='key: pubsub of status updates [default: {}]'.format(status_queue))

    # MinIO
    parser.add_argument(
        '--minio-host', default='localhost',
        help='host name/address of minio [default: localhost]'
    )
    parser.add_argument(
        '--minio-port', type=int, default=9000,
        help='port of minio [default: 9000]'
    )
    parser.add_argument(
        '--minio-access-key',
        help='access key of minio'
    )
    parser.add_argument(
        '--minio-secret-key',
        help='secret key of minio'
    )
    parser.add_argument(
        '--minio-secure', action='store_true',
        help='HTTPS connection to minio [default: false]'
    )

    conf = parser.parse_args()

    if conf.verbose:
        logger.setLevel(logging.DEBUG)

    redis_client = redis.Redis(host=conf.redis_host, port=conf.redis_port,
                               db=conf.redis_db, password=conf.redis_password)

    if task_queue:
        task_queue = TaskQueue(redis=redis_client, key=conf.redis_task_queue)

    status_queue = StatusQueue(redis=redis_client, key=conf.redis_status_queue)

    minio_client = minio.Minio(conf.minio_host + ':' + str(conf.minio_port),
                               conf.minio_access_key, conf.minio_secret_key,
                               secure=conf.minio_secure)

    return conf, task_queue, status_queue, minio_client


class TaskQueue:
    def __init__(self, redis, key):
        self._redis = redis
        self._key = key

    def listen(self):
        continued = False

        while True:
            task = self._wait_for_task(timeout=1, continued=continued)

            # task found in `timeout` seconds, handle it ...
            if task:
                logger.debug('Handling task ...')
                yield(task)
                continued = False
            else:
                # no task found until timeout
                # here the OS can handle keyboard interruption
                continued = True

    def _wait_for_task(self, timeout=0, continued=True):
        """ Wait for a new entry in redis queue (list with left pop and right push)
            of key `redis_key` in database of connection `r`.
        """

        if not continued:
            logger.debug('Waiting for task ...')

        # block until command can be taken from queue or timeout is reached
        raw_command = self._redis.blpop(self._key, timeout)

        if not raw_command:
            return None

        logger.debug('Received command {}'.format(raw_command))

        try:
            command = json.loads(raw_command[1])
        except Exception as e:
            logger.error(
                'Invalid Entry in Task Queue "{}": {}'.format(self._key, e))
            return None

        return command

    def submit(self, task):
        self._redis.rpush(self._key, json.dumps(task))


class StatusQueue:
    def __init__(self, redis, key):
        self._redis = redis
        self._key = key

    def submit(self, status):
        self._redis.publish(self._key, json.dumps(status))

    def listen(self):
        pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(self._key)

        for status in pubsub.listen():
            yield(json.loads(status))
