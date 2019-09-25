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

            log_file_handler = open("/log.txt", "w")
            log_file_handler.write("Starting to process the received task \n")
            log_file_handler.write("{}\n".format(task))

            status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.IN_PROGRESS,
                                            training_id=task.training_id, message="Task in progress"))

            print("All needed parameters are available. Processing continues.")
            print(task.resources)

            download_results = []

            log_file_handler.write("Starting to download all needed files. \n")
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
                    log_file_handler.write("While the task was processed, the following error has occurred: \n")
                    log_file_handler.write("############################################################### \n")
                    log_file_handler.write("At least one download failed. Task failed!\n")
                    status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Download failed"))
            log_file_handler.write("All needed files were successfully downloaded. Processing continues \n")

            # Step 2.1: Merge all corpus-files into one final corpus and save the file locally
            try:
                log_file_handler.write("Starting to merge all downloaded corpus-files. \n")
                corpus = merge_corpus_list(corpus_list, log_file_handler)
            except Exception as e:
                print(e)
                log_file_handler.write("While all corpus files were merged into one, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("Either the given list is empty, or it was not possible to open a given corpus file. \n")
                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Corpus merge failed"))

            # Step 2.2: Save merged corpus file locally
            try:
                log_file_handler.write("Successfully merged all corpus-files. Continuing by saving the merged corpus locally \n")
                save_txt_file("/data_prep_worker/out/corpus.txt", corpus)
            except Exception as e:
                print(e)
                log_file_handler.write("While the merged corpus list was saved locally, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to save the file. \n")
                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Saving merged corpus file locally failed"))
            log_file_handler.write("Successfully saved the merged corpus file \n")

            # Step 3.1: Create the unique word list by using the combined corpus
            try:
                log_file_handler.write("Processing continues. Next step is to create a unique word list \n")
                lexicon = create_unique_word_list("/data_prep_worker/out/corpus.txt")
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to create the unique word list, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to open the corpus-file correctly. Therefore, it was not possible to create the unique word list \n")
                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Unique word list creation failed"))
            log_file_handler.write("Successfully created the unique word list. \n")

            # Step 3.2: Save the unique word list locally
            try:
                log_file_handler.write("Saving the word list locally, before the processing continues. \n")
                save_txt_file("/data_prep_worker/out/final_word_list", lexicon)
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to save the unique word list locally, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to save the file. \n")
                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Saving unique word list locally failed"))
            log_file_handler.write("Successfully saved the word list. \n")

            # Step 4: Execute Phonetisaurus and create phones for the unique word
            try:
                log_file_handler.write("Processing continues by executing the Phonetisaurus which will create the lexicon-file for the Kaldi-Framework. \n")
                execute_phonetisaurus()
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to execute the Phonetisaurus, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was either not possible to read the unique word list properly, or an error occured while executing the Phonetisaurus! \n")
                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Failing while executing the Phonetisaurus"))
            log_file_handler.write("Successfully created the lexicon-file. \n")
            print("Successfully created the lexicon-file")

            # Step 5: Upload of lexicon.txt, corpus.txt and unique_word_list files
            log_file_handler.write("Processing continues by uploading the created lexicon-file and merged corpus to their corresponding MinIO-bucket \n")
            lexicon_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"], 
                                              "{}/lexicon.txt".format(task.training_id), "/data_prep_worker/out/lexicon.txt")

            corpus_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"], 
                                             "{}/corpus.txt".format(task.training_id), "/data_prep_worker/out/corpus.txt")

            unique_word_list_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"],
                                             "{}/unique_word_list.txt".format(task.training_id), "/data_prep_worker/out/final_word_list")

            if not lexicon_result[0] or not corpus_result[0] or not unique_word_list_result[0]:
                print("At least one upload failed. It is not possible to finish this task successfully.")
                log_file_handler.write("While trying to upload the lexicon.txt and corpus.txt files, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to upload at least one file. Please check your internet connection. \n")
                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="At least one upload failed"))
            log_file_handler.write("Successfully uploaded lexicon.txt and corpus.txt \n")

            # Step 6: Delete all files which were downloaded or created for this task
            remove_local_files("/data_prep_worker/in/")
            remove_local_files("/data_prep_worker/out/")

            log_file_handler.close()
            logfile_result = upload_to_bucket(minio_client, minio_buckets["LOG_BUCKET"], "data_preparation_worker/{}/{}".format(task.training_id, "log.txt"), "/log.txt")
            if not logfile_result[0]:
                print("An error occurred during the upload of the logfile.")
            print("Logfile was successfully uploaded")

            #TODO: Create stats-files for the frontend

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
