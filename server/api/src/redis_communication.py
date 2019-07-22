import json
from config import redis_client
from minio_communication import minio_buckets
from redis_config import redis_queues

def create_textprep_job(resourcename, filetype):
    '''
    Creates a new job in the queue for a text preperation worker.
    '''
    entry = {
        "text" : resourcename,
        "type" : filetype.name
    }
    redis_client.rpush(redis_queues["TEXT_PREP_QUEUE"], json.dumps(entry))
    return


def create_g2p_job(uniquewordlists, language_model='Voxforge'):
    '''
    Creates a new job in the queue for a g2p worker.
    '''
    entry = {
        "bucket-in" : minio_buckets["G2P_IN_BUCKET"],
        "bucket-out" : minio_buckets["G2P_OUT_BUCKET"],
        "language_model" : language_model,
        "uniquewordlists" : [wl.name for wl in uniquewordlists]
    }
    redis_client.rpush(redis_queues["G2P_QUEUE"], json.dumps(entry))
    return