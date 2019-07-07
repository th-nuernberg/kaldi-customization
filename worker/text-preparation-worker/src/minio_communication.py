import minio
from minio import ResponseError


def download_from_bucket(minio_client, bucket, filename, target_path):
    try:
        print(minio_client.fget_object(bucket, filename, target_path + filename))

    except ResponseError as err:
        print(err)
        return (False, err)
    return (True, "")


def upload_to_bucket(minio_client, bucket, object_name, file_path):
    # Put an object 'myobject' with contents from '/tmp/otherobject'
    # upon success prints the etag identifier computed by server.
    try:
        print(minio_client.fput_object(bucket, object_name, file_path))
    except ResponseError as err:
        print(err)
        return (False, err)
    return (True, "")