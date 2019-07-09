import json
import os
import redis
from data_processing import execute_phonetisaurus, merge_word_lists, merge_corpus_list
from minio_communication import download_from_bucket, upload_to_bucket
from minio import Minio
from minio import ResponseError


def report_status_to_API(queue_status, conn, filename, message):
    pass


def infinite_loop():
    conn = redis.Redis(host='redis', port=6379, db=0, password="kalditproject")
    minio_client = Minio('minio:9000',
                         access_key='AKIAIOSFODNN7EXAMPLE',
                         secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                         secure=False)
    while True:
        data = conn.blpop('Data-Prep-Queue', 1)
        if data:
            print("Received the following task from Data-Prep-Queue: ")
            print(data)
            try:
                #TODO: Update status queue and set task to: In Progress
                json_data = json.loads(data[1])
                print("Starting to process received data")

                if "bucket_in" in json_data and "bucket_out" in json_data and "lexicon" in json_data and "uniquewordlists" in json_data and "corpuslist" in json_data:
                    # TODO: Print a message if all parameters are correctly recieved, else update status queue to: Failure
                    
                    bucket_in = json_data["bucket-in"]
                    bucket_out = json_data["bucket-out"]
                    lexicon = json_data["lexicon"]
                    word_lists = json_data["uniquewordlists"]
                    #TODO: Corpuslist is still missing
                    corpus_list = json_data["corpuslist"]
                    #TODO: Acoustic bucket is still missing. This bucket is needed in order to retrieve the lexicon file

                    # Step 1: Download all files which were created by the Text-Preparation-Worker for this task:
                    #           -  All word lists
                    #           -  All corpuses 
                    #TODO: Not all necessary files are downloaded yet (corpus list is missing)
                    download_from_bucket(minio_client, bucket_in, lexicon, "/data_prep_worker/in/")
                    for word_list in word_lists:
                        download_from_bucket(minio_client, bucket_in, word_list, "/data_prep_worker/in/")
                    
                    # Step 2: Merge all word lists into one 
                    merge_word_lists(word_lists)

                    # Step 3: Merge all corpuses into one 
                    merge_corpus_list(corpus_list)
                    
                    # Step 4: Execute Phonetisaurus and create phones for the unique word list of all files
                    execute_phonetisaurus(lexicon)

                    # Step 5: Upload lexicon which was retrieved by phonetisaurus-apply and its graph
                    #TODO: Upload final_word_list_with_phones
                    #TODO: Upload final_corpus 
                    #TODO: Check whether the upload is successfull
                    upload_to_bucket(minio_client, bucket_out, "model.fst", "/data_prep_worker/out/")
                    for word_list in word_lists:
                        upload_to_bucket(minio_client, bucket_out, word_list, "/data_prep_worker/out/")

                    #Step 6: Update status queue to: Successfull if this point is reached
                    #TODO: Update status queue 
            except:
                # Received parameters are wrong --> Update status queue and set task processing to: failure
                report_status_to_API(queue_status=12, conn=conn, filename="failure", message="Data is not valid JSON. Processing cancelled")

if __name__ == "__main__":
    print("Data-Preparation-Worker starts running")
    infinite_loop()
    print("Data-Preparation-Worker stops running")