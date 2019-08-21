import json
import minio
import sys
from minio import Minio
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets


def copy_from_resource_to_training_resource(minio_client):

    for i in range(1, 7, 1):
        download_from_bucket(
            minio_client=minio_client,
            bucket=minio_buckets["RESOURCE_BUCKET"],
            filename="{}/corpus.txt".format(i),
            target_path="/{}.txt".format(i))
        upload_to_bucket(
            minio_client=minio_client,
            bucket=minio_buckets["TRAINING_RESOURCE_BUCKET"],
            filename="{}/corpus.txt".format(i),
            file_path="/{}.txt".format(i))


if __name__ == "__main__":
    minio_host = sys.argv[1]
    minio_access_key = sys.argv[2]
    minio_secret_key = sys.argv[3]

    minio_client = Minio(minio_host + ":9000", minio_access_key, minio_secret_key, secure=False)

    copy_from_resource_to_training_resource(minio_client)