import redis
import sys
import minio
import json
from minio import Minio


def test_text_prep_with_valid_json():
    # Step 1: Create redis tasks for the following file types:
    text_file_task = {
        "resource_uuid": "1",
        "file_type" : "txt"
    }

    # Step 2: Subscribe to the status-queue channel
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('Status-Queue')

    # Step 3: Send all tasks for text-prep-worker into the queue
    redis_client.rpush('Text-Prep-Queue', json.dumps(text_file_task))

    # Step 4: Listen to all incoming Status-queue messages
    for msg in pubsub.listen(): 
        print("Received the following message via Status-Queue")
        print(msg)
        data_part = json.loads(msg['data'])
        if data_part['id'] == 10:
            return 0
        else:
            return 999

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
    return_value = test_text_prep_with_valid_json()
    if return_value == 0:
        print("Test was finished successfully. Exiting with code 0.")
        exit(0)
    else:
        print("Test failed. Exiting with code 999")
        exit(999)