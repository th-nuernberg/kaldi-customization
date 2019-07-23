#!/usr/bin/python
import json
import os

from connector import *
from data_processing import (execute_phonetisaurus, merge_word_lists,
                             merge_corpus_list, remove_local_files)
from minio_communication import download_from_bucket, upload_to_bucket, minio_buckets



def report_status_to_API(queue_status, status_queue, filename=None, message=None):
    '''
    By calling this function the status queue is updated.
    Possible updates for the status queue are:
        - InProgress --> queue_status = 21
        - Success    --> queue_status = 200
        - Failure    --> queue_status = 22
    As soon as the Data-Preparation-Worker receives a new task, its entry
    within the Status-Queue is updated to: In-Progress.
    Depending on the processing result, the status of the task can change into:
        - Success
        - Failure
    '''
    if queue_status == 21 and not message:
        message = "Task in progress"
    elif queue_status == 22 and not message:
        message == "Task has failed"
    elif queue_status == 200 and not message:
        message = "Task finished successfully"

    status_queue.submit({"type": "text-prep", "text": filename, "status": queue_status, "msg": message})


def are_parameters_missing(json_data):
    '''
    This function checks whether a needed parameter is missing. 

    If one or more parameters are missing, the function will return: (True, message), where message
    contains the missing parameters.

    If no parameter is missing, the function will return: (False, "").
    '''

    parameter_list = ["resources", "acoustic-model", "id"]
    missing_list = []

    for parameter in parameter_list:
        if parameter not in json_data:
            missing_list.append(parameter)

    if len(missing_list) == 0:
        return (False, "")

    if len(missing_list) == 1:
        return (True, "The following parameter is missing: " + missing_list[0])
    elif len(missing_list) == 2:
        return (True, "The following parameters are missing: " + missing_list[0] + " and " + missing_list[1])
    elif len(missing_list) > 2:
        message = "The following parameters are missing: " + missing_list[0] + ", "
        for i in range(1, len(missing_list), 1):
            if i == len(missing_list) - 1:
                message += " and " + missing_list[i]
            elif i == len(missing_list) -2 :
                message += missing_list[i]
            else:
                message += missing_list[i] + ", "
    return (True, message)


def infinite_loop():
    _ , task_queue, status_queue, minio_client = parse_args('Data-Preparation-Worker Connector', task_queue='Data-Prep-Queue')

    for data in task_queue.listen():
        print("Received the following task from Data-Prep-Queue: ")
        print(data)
        try:
            #TODO: Update status queue and set task to: In Progress
            report_status_to_API(queue_status=21, status_queue=status_queue, filename="In-Progress")

            print("Starting to process received data")
            missing, message = are_parameters_missing(data)

            if not missing:
                print("All needed parameters are available. Processing continues.")
                resources = data["resources"]
                acoustic_model = data["acoustic-model"]
                id = data["id"]
                print(resources)
                
                download_results = []

                # Step 1: Download all files which were created by the Text-Preparation-Worker for this task:
                # Download of the models lexicon and graph
                download_results.append(download_from_bucket(minio_client, minio_buckets["ACOUSTIC_MODELS_BUCKET"],
                                        acoustic_model + "/g2p_model.fst" ,"/data_prep_worker/in/g2p_model.fst"))

                word_lists = list()
                corpus_list = list()
                for resource in resources:
                    # Download of all corpus files which were created within the TPW
                    loc_corp_path = "/data_prep_worker/in/" + resource + "_corpus.txt"
                    download_results.append(download_from_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"],
                                            resource + "/corpus.txt" , loc_corp_path))
                    corpus_list.append(loc_corp_path)

                    # Download of all word lists which were created within the TPW
                    loc_wl_path = "/data_prep_worker/in/" + resource + "_wl.txt"
                    download_results.append(download_from_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"],
                                            resource + "/wl.txt" , loc_wl_path))
                    word_lists.append(loc_wl_path)

                # If any download did not finish --> Set task status to: Failure
                for download in download_results:
                    if not download[0]:
                        print("At least one download did not finish successfully.")
                        #TODO: Update status-queue to: Failure

                # Step 2: Merge all word lists into one 
                merge_word_lists(word_lists)

                # Step 3: Merge all corpuses into one 
                merge_corpus_list(corpus_list)

                # Step 4: Execute Phonetisaurus and create phones for the unique word list of all files
                execute_phonetisaurus()
                print("Finished creating lexicon.txt")

                # Step 5: Upload lexicon which was retrieved by phonetisaurus-apply and its graph
                #TODO: Check whether the upload is successfull
                upload_to_bucket(minio_client, minio_buckets["PROJECT_BUCKET"], id + "/lexicon.txt", "/data_prep_worker/out/lexicon.txt")
                upload_to_bucket(minio_client, minio_buckets["PROJECT_BUCKET"], id + "/corpus.txt", "/data_prep_worker/out/corpus.txt")

                # Step 6: Delete all files which were downloaded or created for this task
                remove_local_files("/data_prep_worker/in/")
                remove_local_files("/data_prep_worker/out/")

                # Step 7: Update status queue to: Successfull if this point is reached
                report_status_to_API(queue_status=200, status_queue=status_queue, filename="success")
            else:
                # At least one parameter is missing --> Update status queue and set task to: Failure
                report_status_to_API(queue_status=22, status_queue=status_queue, filename="failure", message=message)
        except:
            # Received object is not valid JSONO --> Update status queue and set task to: Failure
            report_status_to_API(queue_status=22, status_queue=status_queue, filename="failure", message="Data is not valid JSON. Processing cancelled")


if __name__ == "__main__":
    print("Data-Preparation-Worker starts running")
    infinite_loop()
    print("Data-Preparation-Worker stops running")