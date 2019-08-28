import redis
import sys
import minio
import json
from minio import Minio
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets


def test_decode_worker(redis_client, minio_client):
    # Step 1: Subscribe to the status-queue
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("Status-Queue")

    # Step 2: Create JSON object which will be used for the data-prep-queue
    '''
    task = {
        'decode_file': 'test.wav',
        'acoustic_model_id': '1',
        'training_id': 'test'
    }
    '''
    task2 = {
        'decode_file': 'test2.wav',
        'decode_uuid': 'ICH BIN EINE UUID',
        'acoustic_model_id': '1',
        'training_id': 'test'
    }

    # Step 3: Send task into the data-prep-queue
    # redis_client.rpush('Decoding-Queue', json.dumps(task))
    redis_client.rpush('Decoding-Queue', json.dumps(task2))

    # Step 4: Check which responses are returned over the status-queue from the data-prep-worker
    exit_code = 0
    for msg in pubsub.listen():
        print("Received the following messages:")
        print(msg)
        data_part = json.loads(msg['data'])
        if data_part['id'] == 100:
            pass
        elif data_part['id'] == 200:
            print("Test task finished successfully.")
            print("Exiting Data-Preparation-Tester with exit code 0")
            break
        else:
            print("Test task did not finish successfully.")
            print("Exiting Data-Preparation-Tester with exit code 999")
            exit_code = 999
            break
    exit(exit_code)


if __name__ == "__main__":
    redis_host = sys.argv[1]
    redis_password = sys.argv[2]
    minio_host = sys.argv[3]
    minio_access_key = sys.argv[4]
    minio_secret_key = sys.argv[5]

    print("Setting up connection to Redis and MinIO.")
    redis_client = redis.Redis(host=redis_host, password=redis_password)
    minio_client = Minio(minio_host + ":9000", minio_access_key, minio_secret_key, secure=False)
    print("Finished setting up connection to Redis and MinIO.")
    print("Test process starting.")
    test_decode_worker(redis_client, minio_client)
