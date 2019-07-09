import minio
from minio import ResponseError


def download_from_bucket(minio_client, bucket, filename, target_path):
    try:
        minio_client.fget_object(bucket, filename, target_path + filename)
    except ResponseError as err:
        print(err)
        return (False, err)

    print("Download of " + filename + " was successfull.")
    return (True, "")


def upload_to_bucket(minio_client, bucket, filename, file_path):
    try:
        minio_client.fput_object(bucket, filename, file_path + filename)
    except ResponseError as err:
        print(err)
        return (False, err)

    print("Upoad of " + filename + " was successfull.")
    return (True, "")
