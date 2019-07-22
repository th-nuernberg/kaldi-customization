import redis
import sys
import unittest
import minio
import json
from minio import Minio
from minio_communication import upload_to_bucket, download_from_bucket


def test_text_prep(redis_client, minio_client):
    # Step 1: Create texts-in and texts-out bucket
    try:
        minio_client.make_bucket("texts-in")
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.ResponseError as e:
        raise e
    try:
        minio_client.make_bucket("texts-out")
    except (minio.error.BucketAlreadyOwnedByYou, minio.error.BucketAlreadyExists):
        pass
    except minio.ResponseError as e:
        raise e
    # Step 2: Upload needed files into the texts-in bucket
    upload_to_bucket(minio_client, "texts-in", "kafkatxt", "test-files/txt/")
    upload_to_bucket(minio_client, "texts-in", "kafkapdf", "test-files/pdf/")
    upload_to_bucket(minio_client, "texts-in", "kafkadocx", "test-files/word/")
    upload_to_bucket(minio_client, "texts-in", "gamestarhtml", "test-files/html/")
    upload_to_bucket(minio_client, "texts-in", "dokumentjpg", "test-files/jpg/")
    upload_to_bucket(minio_client, "texts-in", "dokumentpng", "test-files/png/")
    # Step 3: Create redis tasks for the following file types:
    #      3.1: txt-file
    text_file_task = {
        "text" : "kafkatxt",
        "type" : "txt"
    }
    #      3.2: PDF-file
    pdf_file_task = {
        "text" : "kafkapdf",
        "type" : "pdf"
    }
    #      3.3: docx-file
    docx_file_task = {
        "text" : "kafkadocx",
        "type" : "docx"
    }
    #      3.4: jpg image
    jpg_file_task = {
        "text" : "dokumentjpg",
        "type" : "jpg"
    }
    #      3.5: png image
    png_file_task = {
        "text" : "dokumentpng",
        "type" : "png"
    }
    #      3.6: html-file
    html_file_task = {
        "text" : "gamestarhtml",
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

