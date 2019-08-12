import sys
from minio_communication import *
from minio import Minio


def create_all_buckets(minio_client):
    minio_client.make_bucket("resources")
    minio_client.make_bucket("training-resources")
    minio_client.make_bucket("decodings")
    minio_client.make_bucket("acoustic-models")
    minio_client.make_bucket("trainings")


def upload_all_text_prep_files(minio_client):
    '''
    The following files are needed for the Text-Preparation-Worker:
        - txt-file
        - docx-file
        - pdf-file
        - png-file
        - jpg-file
        - html-file

    All these files need to be saved within the resources bucket
    '''
    pass


def upload_all_data_prep_files(minio_client):
    '''
    The following files are needed for the Data-Preparation-Worker:
        - acoustic model == g2p_model.fst

    The acoustic model needs to be uploaded to the acoustic-models bucket
    '''
    pass


def upload_all_files_for_kaldi(minio_client):
    '''
    The following files are needed for the Kaldi-Worker:
        -

    The acoustic model needs to be uploaded to the acoustic-models bucket

    The following files are needed for the Decode-Worker:
        - 
    
    The acoustic model needs to be uploaded to the acoustic-models bucket
    '''
    pass


if __name__ == "__main__":
    # Step 1: Setup connection to MinIO-server
    print("Setting up connection to MinIO-server")
    redis_host = sys.argv[1]
    redis_password = sys.argv[2]
    minio_host = sys.argv[3]
    minio_access_key = sys.argv[4]
    minio_secret_key = sys.argv[5]

    minio_client = Minio(minio_host + ":9000", minio_access_key, minio_secret_key, secure=False)
    print("Established connection to MinIO-server")
    print("")

    # Step 2: Creating all necessary buckets 
    print("Starting to create all needed buckets")
    create_all_buckets(minio_client)
    print("All buckets were successfully created")
    print("")

    # Step 3: Uploading all necessary files for text-preparation-worker
    print("Starting to upload all necessary files for the Text-Preparation-Worker")
    upload_all_text_prep_files(minio_client)
    print("All necessary files were successfully uploaded")
    print("")

    # Step 4: Uploading all necessary files for data-preparation-worker
    print("Starting to upload all necessary files for the Data-Preparation-Worker")
    upload_all_data_prep_files(minio_client)
    print("All necessary files were successfully uploaded")
    print("")

    # Step 5: Uploading all necessary files for kaldi-worker and decode-worker
    print("Starting to upload all necessary files for the Kaldi-worker and Decode-worker")
    upload_all_files_for_kaldi(minio_client)
    print("All necessary files were successfully uploaded")
    print("")
