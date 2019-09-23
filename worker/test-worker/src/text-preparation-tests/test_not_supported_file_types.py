import redis
import sys
import minio
import json
from minio import Minio


def test_text_prep(redis_client, minio_client):
    # Step 1: Create redis tasks for the following file types:
    #      1.1: txt-file
    dll_file_task = {
        "resource_uuid": "1",
        "file_type" : "dll"
    }

    # Step 2: Subscribe to the status-queue channel
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('Status-Queue')

    # Step 3: Send all tasks for text-prep-worker into the queue
    redis_client.rpush('Text-Prep-Queue', json.dumps(dll_file_task))

    # Step 4: Listen to all incoming Status-queue messages
    count = 0
    for msg in pubsub.listen(): 
        print("Received the following message via Status-Queue")
        print(msg)
        data_part = json.loads(msg['data'])
        if data_part['id'] == 100:
            exit(0)
        elif data_part['id'] == 200:
            exit(999)
        else:
            pass




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
    test_text_prep(redis_client, minio_client)
