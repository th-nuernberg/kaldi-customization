import redis
import sys
import minio
import json
from minio import Minio
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets


def test_text_prep(redis_client, minio_client):
    # Step 1: Create redis tasks for the following file types:
    #      1.1: txt-file
    text_file_task = {
        "resource_uuid": "1",
        "file_type" : "txt"
    }
    #      1.2: PDF-file
    pdf_file_task = {
        "resource_uuid": "2",
        "file_type" : "pdf"
    }
    #      1.3: docx-file
    docx_file_task = {
        "resource_uuid": "3",
        "file_type" : "docx"
    }
    #      1.4: jpg image
    jpg_file_task = {
        "resource_uuid": "5",
        "file_type" : "jpg"
    }
    #      1.5: png image
    png_file_task = {
        "resource_uuid": "6",
        "file_type" : "png"
    }
    #      1.6: html-file
    html_file_task = {
        "resource_uuid": "4",
        "file_type" : "html"
    }

    # Step 2: Subscribe to the status-queue channel
    pubsub = redis_client.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('Status-Queue')

    # Step 3: Send all tasks for text-prep-worker into the queue
    redis_client.rpush('Text-Prep-Queue', json.dumps(text_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(pdf_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(docx_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(jpg_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(png_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(html_file_task))


    '''
    {'type': 'message', 'pattern': None, 'channel': b'Status-Queue', 
    'data': b'{"__queue__": "text_prep", "id": 200, "message": "Task finished successfully", "resource_uuid": "1"}'}
    '''
    # Step 4: Listen to all incoming Status-queue messages
    count = 0
    for msg in pubsub.listen(): 
        print("Received the following message via Status-Queue")
        print(msg)
        data_part = json.loads(msg['data'])
        if data_part['id'] == 200:
            count += 1
        if count == 6:
            print("All tasks finished successfully")
            break
    exit(0)




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

