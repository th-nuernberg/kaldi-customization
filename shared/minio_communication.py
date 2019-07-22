import minio
from minio import ResponseError

minio_buckets = dict(
    # MinIO Bucket definitions
    # text-prep-worker
    TEXTS_IN_BUCKET='texts-in',
    TEXTS_OUT_BUCKET='texts-out',

    # G2P-worker
    G2P_IN_BUCKET  = 'g2p-in',
    G2P_OUT_BUCKET = 'g2p-out',

    # acoustic models thfilenameat are trained by users
    ACOUSTIC_MODELS_BUCKET  = 'acoustic-models',
    # predefined models and stuff for kaldi like vocabular
    LANGUAGE_MODELS_BUCKET  = 'language-models')

def does_bucket_exist(minio_client, bucket_name):
    try:
        minio_client.bucket_exists(bucket_name)
    except ResponseError as err:
        print(err)
        return (False, err)
    print("Requested bucket exists.")
    return (True, "")


def download_from_bucket(minio_client, bucket, filename, target_path):
    try:
        minio_client.fget_object(bucket, filename, target_path)
            
    except ResponseError as err:
        print(err)
        return (False, err)

    print("Download of " + filename + " was successfull.")
    return (True, "")


def upload_to_bucket(minio_client, bucket, filename, file_path):
    try:
        minio_client.fput_object(bucket, filename, file_path)
    except ResponseError as err:
        print(err)
        return (False, err)

    print("Upload of " + filename + " was successfull.")
    return (True, "")
