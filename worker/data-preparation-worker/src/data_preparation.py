# -*- encoding: utf-8 -*-
#!/usr/bin/python
import json
import os

from connector import *
from data_processing import (execute_phonetisaurus, merge_corpus_list,
                             remove_local_files, save_txt_file, create_unique_word_list)
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets


def infinite_loop():
    _, task_queue, status_queue, minio_client = parse_args(
        'Data-Preparation-Worker Connector', task_queue='Data-Prep-Queue')

    for data in task_queue.listen():
        print("Received the following task from Data-Prep-Queue: ")
        print(data)

        task = None

        try:
            print("Starting to process received data")
            task = DataPrepTask(**data)

            status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.IN_PROGRESS,
                                            training_id=task.training_id, message="Task in progress"))

            print("All needed parameters are available. Processing continues.")
            print(task.resources)

            download_results = []

            # Step 1: Download all files which were created by the Text-Preparation-Worker for this task.
            #         In addition to that, download the G2P-graph from the acoustic-bucket:
            # Download of the graph
            download_results.append(download_from_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"],
                                                        "{}/g2p_model.fst".format(task.acoustic_model_id), "/data_prep_worker/in/g2p_model.fst"))

            corpus_list = list()
            for resource in task.resources:
                # Download of all corpus files which were created within the TPW
                loc_corp_path = "/data_prep_worker/in/{}_corpus.txt".format(
                    resource)
                download_results.append(download_from_bucket(minio_client, minio_buckets["TRAINING_RESOURCE_BUCKET"],
                                                            "{}/corpus.txt".format(resource), loc_corp_path))
                corpus_list.append(loc_corp_path)

            # If any download did not finish --> Set task status to: Failure
            for download in download_results:
                if not download[0]:
                    status_queue.submit(DataPrepStatus(
                        id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Download failed"))

            # Step 2: Merge all corpus-files into one final corpus and save the file locally
            corpus = merge_corpus_list(corpus_list)
            save_txt_file("/data_prep_worker/out/corpus.txt", corpus)

            # Step 3: Create the lexicon file by using the combined corpus
            lexicon = create_unique_word_list(
                "/data_prep_worker/out/corpus.txt")
            save_txt_file("/data_prep_worker/out/final_word_list", lexicon)

            # Step 4: Execute Phonetisaurus and create phones for the unique word
            execute_phonetisaurus()
            print("Finished creating lexicon.txt")

            # Step 5: Upload lexicon which was retrieved by phonetisaurus-apply and its graph
            # TODO: Check whether the upload is successfull
            upload_to_bucket(
                minio_client, minio_buckets["TRAINING_BUCKET"], "{}/lexicon.txt".format(task.training_id), "/data_prep_worker/out/lexicon.txt")
            upload_to_bucket(
                minio_client, minio_buckets["TRAINING_BUCKET"], "{}/corpus.txt".format(task.training_id), "/data_prep_worker/out/corpus.txt")

            # Step 6: Delete all files which were downloaded or created for this task
            remove_local_files("/data_prep_worker/in/")
            remove_local_files("/data_prep_worker/out/")

            # Step 7: Update status queue to: Successfull if this point is reached
            status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.SUCCESS,
                                               training_id=task.training_id, message="Task finished successfully"))
        except Exception as e:
            status_queue.submit(DataPrepStatus(
                id=DataPrepStatusCode.FAILURE,
                training_id=task.training_id if task else None,
                message=str(e)
            ))
            raise e


if __name__ == "__main__":
    print("Data-Preparation-Worker starts running")
    infinite_loop()
    print("Data-Preparation-Worker stops running")
