#!/usr/bin/python

import minio
import redis
import unittest

from util import logger, logging, parse_args, TaskQueue


class TestKaldiWorker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._redis = redis.Redis(port=6380, password='kalditproject')
        cls._task_queue = 'Test-Redis-Queue'

    @classmethod
    def setUp(cls):
        cls._redis.delete(cls._task_queue)

    @classmethod
    def tearDownClass(cls):
        del cls._redis

    def test_receive_task(self):
        queue = TaskQueue(redis=self._redis, key=self._task_queue)
        queue.submit(r'{"message": "Test"}')
        task = next(queue.listen())
        print(task)
        self.assertIsNotNone(task)


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    unittest.main()
