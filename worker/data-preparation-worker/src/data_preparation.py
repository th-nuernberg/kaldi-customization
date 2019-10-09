# -*- encoding: utf-8 -*-
#!/usr/bin/python
import json
import os

from connector import *
from data_processing import (execute_phonetisaurus, merge_corpus_list, combine_old_and_new_lexicon_files,
                             remove_local_files, save_txt_file, create_unique_word_list, compare_lexicon_with_word_list,
                             gather_corpus_information, save_json_file)
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets


def finish_logging(log_file_handler, minio_client, task):
    log_file_handler.close()
    logfile_result = upload_to_bucket(minio_client, minio_buckets["LOG_BUCKET"], "data_preparation_worker/{}/{}".format(task.training_id, "log.txt"), "/log.txt")
    if not logfile_result[0]:
        print("An error occurred during the upload of the logfile.")
    print("Logfile was successfully uploaded")


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
            #         In addition to that, download the G2P-graph and lexicon.txt files from the acoustic-bucket:
            
            # Download of the graph
            download_results.append(download_from_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"],
                                                        "{}/g2p_model.fst".format(task.acoustic_model_id), "/data_prep_worker/in/g2p_model.fst"))
            # Download of the lexicon.txt file
            download_results.append(download_from_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"],
                                                        "{}/lexicon.txt".format(task.acoustic_model_id), "/data_prep_worker/in/lexicon.txt"))
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

                    finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

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

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

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

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Saving merged corpus file locally failed"))
            log_file_handler.write("Successfully saved the merged corpus file \n")

            # Step 3.1: Create the final_word_list, using the combined corpus
            try:
                log_file_handler.write("Processing continues. Next step is to create the final_word_list \n")
                lexicon = create_unique_word_list("/data_prep_worker/out/corpus.txt")                
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to create the final_word_list, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to open the corpus-file correctly. Therefore, it was not possible to create the final_word_list \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Final word list creation failed"))
            log_file_handler.write("Successfully created the final_word_list. \n")

            # Step 3.2: Save the final_word_list locally
            try:
                log_file_handler.write("Saving the word list locally, before the processing continues. \n")
                save_txt_file("/data_prep_worker/out/final_word_list", lexicon)
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to save the final_word_list locally, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to save the file. \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Saving unique word list locally failed"))
            log_file_handler.write("Successfully saved the final_word_list. \n")
                        
            # Step 3.3: Gather all needed stats which are needed for the frontend and create a JSON-file
            try:
                log_file_handler.write("Processing continues by collecting all needed stats for the Frontend! \n")
                number_of_words, number_of_lines = gather_corpus_information("/data_prep_worker/out/corpus.txt")
                number_of_unique_words = len(lexicon)
                number_of_processed_corpus_files = len(corpus_list)
                save_json_file(number_of_words, number_of_lines, number_of_unique_words, number_of_processed_corpus_files)
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to create the final_word_list, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to retrieve all needed information!")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Failed to retrieve needed stats for the frontend"))
            log_file_handler.write("Successfully retrieved all needed stats for the frontend! \n")

            # Step 4.1: Compare the final_word_list with the existing lexicon.txt file 
            unique_word_list = compare_lexicon_with_word_list(final_word_list="/data_prep_worker/out/final_word_list", lexicon="/data_prep_worker/in/lexicon.txt")

            # Step 4.2: Save the unique_word_list locally 
            save_txt_file(file_path="/data_prep_worker/out/unique_word_list", content_list=unique_word_list)

            # Step 4.3: Execute Phonetisaurus and create phones for the unique_word_list
            try:
                log_file_handler.write("Processing continues by executing the Phonetisaurus which will create the lexicon-file for the Kaldi-Framework. \n")
                execute_phonetisaurus()
            except Exception as e:
                print(e)
                log_file_handler.write("While trying to execute the Phonetisaurus, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was either not possible to read the unique word list properly, or an error occured while executing the Phonetisaurus! \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="Failing while executing the Phonetisaurus"))
            log_file_handler.write("Successfully created the lexicon-file. \n")
            print("Successfully created the lexicon-file")

            # Step 4.4: Append new word and phone list to the lexicon-file
            lexicon = combine_old_and_new_lexicon_files(old_lexicon="/data_prep_worker/in/lexicon.txt", new_lexicon="/data_prep_worker/out/lexicon.txt")

            # Step 4.5: Save final lexicon.txt file locally
            save_txt_file(file_path="/data_prep_worker/out/lexicon.txt", content_list=lexicon)

            # Step 5: Upload of lexicon.txt, corpus.txt and unique_word_list files
            log_file_handler.write("Processing continues by uploading the created lexicon-file and merged corpus to their corresponding MinIO-bucket \n")
            lexicon_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"], 
                                              "{}/lexicon.txt".format(task.training_id), "/data_prep_worker/out/lexicon.txt")

            corpus_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"], 
                                             "{}/corpus.txt".format(task.training_id), "/data_prep_worker/out/corpus.txt")

            unique_word_list_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"],
                                             "{}/unique_word_list.txt".format(task.training_id), "/data_prep_worker/out/final_word_list")

            json_result = upload_to_bucket(minio_client, minio_buckets["TRAINING_BUCKET"],
                                             "{}/stats.json".format(task.training_id), "/data_prep_worker/out/stats.json")

            if not lexicon_result[0] or not corpus_result[0] or not unique_word_list_result[0] or not json_result[0]:
                print("At least one upload failed. It is not possible to finish this task successfully.")
                log_file_handler.write("While trying to upload the lexicon.txt, corpus.txt, unique_word_list.txt and stats.json files, the following error occurred: \n")
                log_file_handler.write("############################################################################# \n")
                log_file_handler.write("It was not possible to upload at least one file. Please check your internet connection. \n")

                finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

                status_queue.submit(DataPrepStatus(id=DataPrepStatusCode.FAILURE, training_id=task.training_id, message="At least one upload failed"))
                continue

            log_file_handler.write("Successfully uploaded lexicon.txt, corpus.txt, unique_word_list.txt and stats.json \n")

            # Step 6: Delete all files which were downloaded or created for this task
            remove_local_files("/data_prep_worker/in/")
            remove_local_files("/data_prep_worker/out/")

            finish_logging(log_file_handler=log_file_handler, minio_client=minio_client, task=task)

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
