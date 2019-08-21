import json
import redis
import sys
import minio
from minio import Minio
from minio_communication import *


def test_data_prep_worker(redis_client, minio_client):
    # Step 1: Create all needed buckets
    try:
        minio_client.make_bucket(minio_buckets["ACOUSTIC_MODELS_BUCKET"])
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.ResponseError as e:
        raise e
    try:
        minio_client.make_bucket(minio_buckets["TRAINING_RESOURCE_BUCKET"])
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.ResponseError as e:
        raise e
    try:
        minio_client.make_bucket(minio_buckets["TRAINING_BUCKET"])
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.ResponseError as e:
        raise e

    # Step 2: Upload all needed files for the data-prep-worker
    # upload_to_bucket(minio_client, bucket, filename, file_path):
    upload_to_bucket(minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], "kafka/corpus.txt", "test-files/kafka_corpus.txt")
    upload_to_bucket(minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"], "text_generator/corpus.txt", "test-files/text_generator_corpus.txt")
    upload_to_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"], "Voxforge-RNN/g2p_model.fst", "test-files/g2p_model.fst")

    # Step 3: Subscribe to the status-queue
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("Status-Queue")

    # Step 4: Create JSON object which will be used for the data-prep-queue
    task = {
        'resources': ['kafka', 'text_generator'],
        'acoustic_model_id': 'Voxforge-RNN',
        'training_id': 'test'
    }

    # Step 5: Send task into the data-prep-queue
    redis_client.rpush('Data-Prep-Queue', json.dumps(task))

    # Step 6: Check which responses are returned over the status-queue from the data-prep-worker
    for msg in pubsub.listen():
        print(msg)


if __name__ == "__main__":
    # Step 0: Setup connection with MinIO and Redis
    redis_host = sys.argv[1]
    redis_password = sys.argv[2]
    minio_host = sys.argv[3]
    minio_access_key = sys.argv[4]
    minio_secret_key = sys.argv[5]

    redis_client = redis.Redis(host=redis_host, password=redis_password)
    minio_client = Minio(minio_host + ":9000", minio_access_key, minio_secret_key, secure=False)
    
    test_data_prep_worker(redis_client, minio_client)
