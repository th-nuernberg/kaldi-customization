import sys
from minio_communication import *
from minio import Minio


def create_all_buckets(minio_client):
    try:
        minio_client.make_bucket("resources")
    except Exception as e:
        pass
    try:
        minio_client.make_bucket("training-resources")
    except Exception as e:
        pass
    try:
        minio_client.make_bucket("decodings")
    except Exception as e:
        pass
    try:
        minio_client.make_bucket("acoustic-models")
    except Exception as e:
        pass
    try:
        minio_client.make_bucket("trainings")
    except Exception as e:
        pass


def upload_all_text_prep_files(minio_client):
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "1/source", "test-files/text_prep_files/txt/kafkatxt")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "2/source", "test-files/text_prep_files/pdf/kafkapdf")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "3/source", "test-files/text_prep_files/word/kafkadocx")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "4/source", "test-files/text_prep_files/html/gamestarhtml")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "5/source", "test-files/text_prep_files/jpg/dokumentjpg")
    upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "6/source", "test-files/text_prep_files/png/dokumentpng")


def upload_all_remaining_files(minio_client):
    voxfore_rnn_id = 1

    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/final.mdl"  , "test-files/remaining_files/voxforge-rnn/final.mdl")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/lexicon.txt"  , "test-files/remaining_files/voxforge-rnn/lexicon.txt")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/tree"  , "test-files/remaining_files/voxforge-rnn/tree")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/phones.txt"  , "test-files/remaining_files/voxforge-rnn/phones.txt")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/g2p_model.fst"  , "test-files/remaining_files/voxforge-rnn/g2p_model.fst")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/cmvn_opts"  , "test-files/remaining_files/voxforge-rnn/cmvn_opts")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.dubm"  , "test-files/remaining_files/voxforge-rnn/extractor/final.dubm")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.ie"  , "test-files/remaining_files/voxforge-rnn/extractor/final.ie")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.ie.id"  , "test-files/remaining_files/voxforge-rnn/extractor/final.ie.id")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.mat"  , "test-files/remaining_files/voxforge-rnn/extractor/final.mat")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/global_cmvn.stats"  , "test-files/remaining_files/voxforge-rnn/extractor/global_cmvn.stats")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/online_cmvn.conf"  , "test-files/remaining_files/voxforge-rnn/extractor/online_cmvn.conf")
    upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/splice_opts"  , "test-files/remaining_files/voxforge-rnn/extractor/splice_opts")

    upload_to_bucket(minio_client,minio_buckets["DECODING_BUCKET"], "test.wav", "test-files/remaining_files/test.wav")
    upload_to_bucket(minio_client,minio_buckets["DECODING_BUCKET"], "test2.wav", "test-files/remaining_files/test2.wav")


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

    # Step 4: Uploading all necessary files for kaldi-worker, decode-worker and data-prep-worker
    print("Starting to upload all necessary files for the Kaldi-worker, Decode-worker and Data-Prep-Worker")
    upload_all_remaining_files(minio_client)
    print("All necessary files were successfully uploaded")
    print("")
