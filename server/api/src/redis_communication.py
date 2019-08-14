import json
from config import redis_client
from minio_communication import minio_buckets
from redis_config import redis_queues


def create_textprep_job(resourcename, filetype):
    '''
    Creates a new job in the queue for a text preperation worker.
    '''
    entry = {
        "resource_uuid": resourcename,
        "file_type": filetype.name
    }

    redis_client.rpush(redis_queues["TEXT_PREP_QUEUE"], json.dumps(entry))


def create_dataprep_job(acoustic_model_id, corpi, training_id):
    '''
    Creates a new job in the queue for a g2p worker.
    '''
    entry = {
        "acoustic_model_id": acoustic_model_id,
        "resources": corpi,
        "training_id": training_id,
    }

    redis_client.rpush(redis_queues["DATA_PREP_QUEUE"], json.dumps(entry))


def create_kaldi_job(training_id, acoustic_model_id):
    '''
    Creates a new job in the queue for a kaldi worker.
    '''

    entry = {
        "training_id": training_id,
        "acoustic_model_id": acoustic_model_id
    }

    redis_client.rpush(redis_queues["KALDI_QUEUE"], json.dumps(entry))


def create_decode_job(decode_file, acoustic_model_id, training_id):
    '''
    Creates a new job in the queue for a decode worker.
    '''

    entry = {
        "decode_file": decode_file,
        "acoustic_model_id": acoustic_model_id,
        "training_id": training_id
    }

    redis_client.rpush(redis_queues["DECODING_QUEUE"], json.dumps(entry))
