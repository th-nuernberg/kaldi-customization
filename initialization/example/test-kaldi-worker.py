import importlib
import importlib.machinery
#importlib.machinery.SourceFileLoader('config','server/api/src/config.py').load_module()
#from config import redis_client
importlib.machinery.SourceFileLoader('redis_config','shared/redis_config.py').load_module()
from redis_config import redis_queues
import redis

import json

redis_client = redis.Redis(host='localhost', port=6380, password='kalditproject')

def create_kaldi_job(project_id,acoustic_model_id):
    '''
    Creates a new job in the queue for a kaldi worker.
    '''

    entry = {
        "project_id" : project_id,
        "acoustic_model_id" : acoustic_model_id
    }
    redis_client.rpush(redis_queues["KALDI_QUEUE"], json.dumps(entry))
    return 0

create_kaldi_job("1","1")