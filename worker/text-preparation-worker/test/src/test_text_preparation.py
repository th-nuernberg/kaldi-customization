import redis
import sys
import unittest
import minio
import json
from minio import Minio
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets


def test_text_prep(redis_client, minio_client):
    # Step 1: Create texts-in and texts-out bucket
    try:
        minio_client.make_bucket(minio_buckets["RESOURCE_BUCKET"])
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.ResponseError as e:
        raise e


    # Step 2: Upload needed files into the texts-in bucket
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "1/kafkatxt", "test-files/txt/kafkatxt")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "2/kafkapdf", "test-files/pdf/kafkapdf")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "3/kafkadocx", "test-files/word/kafkadocx")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "4/gamestarhtml", "test-files/html/gamestarhtml")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "5/dokumentjpg", "test-files/jpg/dokumentjpg")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "6/dokumentpng", "test-files/png/dokumentpng")
    # Step 3: Create redis tasks for the following file types:
    #      3.1: txt-file
    text_file_task = {
        "resource_id": "1",
        "filename" : "kafkatxt",
        "type" : "txt"
    }
    #      3.2: PDF-file
    pdf_file_task = {
        "resource_id": "2",
        "filename" : "kafkapdf",
        "type" : "pdf"
    }
    #      3.3: docx-file
    docx_file_task = {
        "resource_id": "3",
        "filename" : "kafkadocx",
        "type" : "docx"
    }
    #      3.4: jpg image
    jpg_file_task = {
        "resource_id": "5",
        "filename" : "dokumentjpg",
        "type" : "jpg"
    }
    #      3.5: png image
    png_file_task = {
        "resource_id": "6",
        "filename" : "dokumentpng",
        "type" : "png"
    }
    #      3.6: html-file
    html_file_task = {
        "resource_id": "4",
        "filename" : "gamestarhtml",
        "type" : "html"
    }

    # Step 4: Subscribe to the status-queue channel
    pubsub = redis_client.pubsub()
    pubsub.subscribe('Status-Queue')
    
    # Step 5: Send all tasks for text-prep-worker into the queue
    redis_client.rpush('Text-Prep-Queue', json.dumps(text_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(pdf_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(docx_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(jpg_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(png_file_task))
    redis_client.rpush('Text-Prep-Queue', json.dumps(html_file_task))

    # Step 6: Listen to all incoming Status-queue messages
    for msg in pubsub.listen(): print(msg)




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

