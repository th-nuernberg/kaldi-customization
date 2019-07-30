import importlib
import importlib.machinery
#importlib.machinery.SourceFileLoader('config','server/api/src/config.py').load_module()
#from config import redis_client
importlib.machinery.SourceFileLoader('redis_config','shared/redis_config.py').load_module()
from redis_config import redis_queues
import redis

import json

redis_client = redis.Redis(host='localhost', port=6380, password='kalditproject')

def create_decode_job(decode_file,acoustic_model_id,training_id):
    '''
    Creates a new job in the queue for a decode worker.
    '''

    entry = {
        "decode_file" : decode_file,
        "acoustic_model_id" : acoustic_model_id,
        "training_id" : training_id
    }
    redis_client.rpush(redis_queues["DECODING_QUEUE"], json.dumps(entry))
    return 0

create_decode_job("test.wav","1","1")