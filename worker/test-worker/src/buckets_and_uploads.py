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
    try:
        upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "1/source", "test-files/test_worker_files/legal_files/kafkatxt")
    except:
        print("It was not possible to upload 1/source to the RESOURCE_BUCKET. Either the bucket does not exist or the file is not available!")
        return 1

    try:
        upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "2/source", "test-files/test_worker_files/legal_files/kafkapdf")
    except:
        print("It was not possible to upload 2/source to the RESOURCE_BUCKET. Either the bucket does not exist or the file is not available!")
        return 2

    try:
        upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "3/source", "test-files/test_worker_files/legal_files/kafkadocx")
    except:
        print("It was not possible to upload 3/source to the RESOURCE_BUCKET. Either the bucket does not exist or the file is not available!")
        return 3

    try:
        upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "4/source", "test-files/test_worker_files/legal_files/gamestarhtml")
    except:
        print("It was not possible to upload 4/source to the RESOURCE_BUCKET. Either the bucket does not exist or the file is not available!")
        return 4

    try:
        upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "5/source", "test-files/test_worker_files/legal_files/dokumentjpg")
    except:
        print("It was not possible to upload 5/source to the RESOURCE_BUCKET. Either the bucket does not exist or the file is not available!")
        return 5

    try:
        upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], "6/source", "test-files/test_worker_files/legal_files/dokumentpng")
    except:
        print("It was not possible to upload 6/source to the RESOURCE_BUCKET. Either the bucket does not exist or the file is not available!")
        return 6

    return 0


def upload_all_remaining_files(minio_client):
    voxfore_rnn_id = 1

    # Acoustic model file uploads
    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/final.mdl"  , "test-files/remaining_files/voxforge-rnn/final.mdl")
    except:
        print("It was not possible to upload /final.mdl to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 1

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/lexicon.txt"  , "test-files/remaining_files/voxforge-rnn/lexicon.txt")
    except:
        print("It was not possible to upload /lexicon.txt to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 2

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/tree"  , "test-files/remaining_files/voxforge-rnn/tree")
    except:
        print("It was not possible to upload /tree to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 3

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/phones.txt"  , "test-files/remaining_files/voxforge-rnn/phones.txt")
    except:
        print("It was not possible to upload /phones.txt to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 4

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/g2p_model.fst"  , "test-files/remaining_files/voxforge-rnn/g2p_model.fst")
    except:
        print("It was not possible to upload /g2p_model.fst to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 5

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/cmvn_opts"  , "test-files/remaining_files/voxforge-rnn/cmvn_opts")
    except:
        print("It was not possible to upload /cmvn_opts to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 6

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.dubm"  , "test-files/remaining_files/voxforge-rnn/extractor/final.dubm")
    except:
        print("It was not possible to upload /extractor/final.dubm to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 7

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.ie"  , "test-files/remaining_files/voxforge-rnn/extractor/final.ie")
    except:
        print("It was not possible to upload /extractor/final.ie to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 8

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.ie.id"  , "test-files/remaining_files/voxforge-rnn/extractor/final.ie.id")
    except:
        print("It was not possible to upload /extractor/final.ie.id to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 9

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/final.mat"  , "test-files/remaining_files/voxforge-rnn/extractor/final.mat")
    except:
        print("It was not possible to upload /extractor/final.mat to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 10

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/global_cmvn.stats"  , "test-files/remaining_files/voxforge-rnn/extractor/global_cmvn.stats")
    except:
        print("It was not possible to upload /extractor/global_cmvn.stats to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 11

    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/online_cmvn.conf"  , "test-files/remaining_files/voxforge-rnn/extractor/online_cmvn.conf")
    except:
        print("It was not possible to upload /extractor/online_cmvn.conf to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 12
    
    try:
        upload_to_bucket(minio_client,minio_buckets["ACOUSTIC_MODELS_BUCKET"], str(voxfore_rnn_id) + "/extractor/splice_opts"  , "test-files/remaining_files/voxforge-rnn/extractor/splice_opts")
    except:
        print("It was not possible to upload /extractor/splice_opts to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 13

    # Decode file uploads
    try:
        upload_to_bucket(minio_client,minio_buckets["DECODING_BUCKET"], "test.wav", "test-files/remaining_files/test.wav")
    except:
        print("It was not possible to upload test.wav to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 14
    try:
        upload_to_bucket(minio_client,minio_buckets["DECODING_BUCKET"], "test2.wav", "test-files/remaining_files/test2.wav")
    except:
        print("It was not possible to upload test2.wav to the ACOUSTIC_MODELS_BUCKET. Either the bucket does not exist or the file is not available!")
        return 15

    return 0


if __name__ == "__main__":
    # Step 1: Setup connection to MinIO-server
    print("Setting up connection to MinIO-server")
    try:
        redis_host = sys.argv[1]
        redis_password = sys.argv[2]
        minio_host = sys.argv[3]
        minio_access_key = sys.argv[4]
        minio_secret_key = sys.argv[5]

        minio_client = Minio(minio_host + ":9000", minio_access_key, minio_secret_key, secure=False)
        print("Established connection to MinIO-server")
        print("")
    except Exception as e:
        print("It was not possible to establish a connection to the MinIO-server.")
        exit(400)

    # Step 2: Creating all necessary buckets 
    print("Starting to create all needed buckets")
    create_all_buckets(minio_client)
    print("All buckets were successfully created")
    print("")

    # Step 3: Uploading all necessary files for text-preparation-worker
    print("Starting to upload all necessary files for the Text-Preparation-Worker")

    return_value = upload_all_text_prep_files(minio_client)
    if return_value != 0:
        exit(return_value)

    print("All necessary files were successfully uploaded")
    print("")

    # Step 4: Uploading all necessary files for kaldi-worker, decode-worker and data-prep-worker
    print("Starting to upload all necessary files for the Kaldi-worker, Decode-worker and Data-Prep-Worker")
    
    return_value = upload_all_remaining_files(minio_client)
    if return_value != 0:
        exit_value = 100 + return_value
        exit(exit_value)
    
    print("All necessary files were successfully uploaded")
    print("")
    exit(200)
