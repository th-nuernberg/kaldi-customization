import json
import os
import re
import redis
import subprocess
from minio_communication import download_from_bucket, upload_to_bucket
from minio import Minio
from minio import ResponseError


def report_status_to_API(queue_status, conn, filename, message):
    pass


def execute_phonetisaurus(lexicon, word_lists):
    subprocess.call(["phonetisaurus-train", "-l", lexicon, "-s2d", "-g", "-o", "8"])
    
    for word_list in word_lists:
        # Write the new file into the out directory of the g2p_worker
        file_handler = open("/g2p_worker/out/" + word_list, "w")
        # Applies the previously trained graph onto the wordlist
        subprocess.call(["phonetisaurus-apply", "--model", "train/model.fst", "--word_list", "/g2p_worker/in/" + word_list, "-n", "2", "-l", lexicon, "--beam", "10000", "-g", "-t", "10000"], stdout=file_handler)
        file_handler.close()
    # Moves the created graph into the out directory of the g2p_worker
    subprocess.call(["mv", "train/model.fst", "/g2p_worker/out/model.fst"])

def infinite_loop():
    conn = redis.Redis(host='redis', port=6379, db=0, password="kalditproject")
    minio_client = Minio('minio:9000',
                         access_key='AKIAIOSFODNN7EXAMPLE',
                         secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                         secure=False)
    while True:
        data = conn.blpop('G2P-Queue', 1)
        if data:
            print("Received the following task from G2P-Queue: ")
            print(data)
            try:
                json_data = json.loads(data[1])
                print("Starting to process received data")
                if "bucket_in" in json_data and "bucket_out" in json_data and "lexicon" in json_data and "uniquewordlists" in json_data:
                    bucket_in = json_data["bucket-in"]
                    bucket_out = json_data["bucket-out"]
                    lexicon = json_data["lexicon"]
                    word_lists = json_data["uniquewordlists"]

                    # Download all files which are necessary for the G2P process
                    download_from_bucket(minio_client, bucket_in, lexicon, "/g2p_worker/in/")
                    for word_list in word_lists:
                        download_from_bucket(minio_client, bucket_in, word_list, "/g2p_worker/in/")
                    
                    execute_phonetisaurus("g2p_worker/in/" + lexicon, word_lists)

                    # Upload all processed files and Graph
                    upload_to_bucket(minio_client, bucket_out, "model.fst", "/g2p_worker/out/")
                    for word_list in word_lists:
                        upload_to_bucket(minio_client, bucket_out, word_list, "/g2p_worker/out/")

            except:
                # Received parameters are wrong --> Update status queue and set task processing to: failure
                report_status_to_API(queue_status=12, conn=conn, filename="failure", message="Data is not valid JSON. Processing cancelled")

if __name__ == "__main__":
    print("G2P-Worker starts running")
    infinite_loop()
    print("G2P-Worker stops running")
    