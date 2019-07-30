# -*- encoding: utf-8 -*-
#!/usr/bin/python
import json
import os

from connector import *
from file_parser import (pdf_parser, html_parser, word_parser, 
                         text_parser, ocr_parser, generate_corpus)
from minio_communication import download_from_bucket, upload_to_bucket, does_bucket_exist, minio_buckets


def report_status_to_API(queue_status, status_queue, filename=None, message=None):
    '''
    By calling this function the status queue is updated.
    Possible updates for the status queue are:
        - InProgress
        - Success
        - Failure
    As soon as the Text-Preparation-Worker receives a new task, its entry
    within the Status-Queue is updated to: In-Progress.
    Depending on the processing result, the status of the task can change into:
        - Success
        - Failure
    '''
    if queue_status == 11 and not message:
        message = "Task in progress"
    elif queue_status == 12 and not message:
        message == "Task has failed"
    elif queue_status == 200 and not message:
        message = "Task finished successfully"

    status_queue.submit({"type": "text-prep", "text": filename, "status": queue_status, "msg": message})


def save_textfile(text_list, filename):
    '''
    This function saves the created corpus into the file system as a txt-file
    The following directory will be used to save the corpus:
        /text-preparation/out/<filename>.txt
    '''

    file_handler = open("/text_prep_worker/out/" + filename, "w")
    for sentence in text_list:
        file_handler.write(sentence + "\n")
    file_handler.close()


def remove_local_files(path):
    text_prep_in_files = os.listdir(path)    
    for file in text_prep_in_files:
        os.remove(path + file)

def process_file(file_type, filename, resource_id, minio_client):
    '''
    This function is called, in order to open the received filename of the API.
    All files which need to be processed are saved within:
        /text-preparation/in/<filename>
    The following file types are supported:
        - PDF
        - Docx
        - HTML
        - txt
        - PNG or JPG
    '''
    text_prep_input = "/text_prep_worker/in/"
    text_prep_output = "/text_prep_worker/out/"

    # Step 1: Checks whether the requested bucket exist
    existance_result_in = does_bucket_exist(minio_client, minio_buckets["RESOURCE_BUCKET"])
    if not existance_result_in[0]:
        return existance_result_in

    # Step 2: Downloads the needed file which is located within the texts-in bucket
    download_result = download_from_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], resource_id + "/" + filename, text_prep_input + filename)
    if not download_result[0]:
        return download_result

    # Step 3: Process the downloaded file
    #         After processing the corpus is ready
    file_path = text_prep_input + filename
    full_text = ""
    try:
        if file_type == "pdf":
            full_text = pdf_parser(file_path)
        elif file_type == "docx":
            full_text = word_parser(file_path)
        elif file_type == "html":
            full_text = html_parser(file_path)
        elif file_type == "txt":
            full_text = text_parser(file_path)
        elif file_type == "png" or file_type == "jpg":
            full_text = ocr_parser(file_path)            
        else:
            return (False, "Given file type is not supported. Finishing processing")

        # Generates the corpus
        corpus = generate_corpus(full_text)

    except Exception as e:
        print(e)
        return (False, "Failed to parse given file")

    # Step 4: Save corpus locally 
    try:
        corpus_name = filename + "_corpus"
        save_textfile(corpus, corpus_name)
    except:
        return (False, "Failed to save corpus")

    # Step 5: Upload corpus in bucket 
    corpus_path = text_prep_output + corpus_name
    corpus_upload_result = upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], resource_id + "/corpus.txt", corpus_path)
    if not corpus_upload_result[0]:
        return corpus_upload_result

    # Step 6: Remove local files 
    remove_local_files(text_prep_input)
    remove_local_files(text_prep_output)
    
    return (True, "Processing of data has finished successfully")


def infinite_loop():

    _ , task_queue, status_queue, minio_client = parse_args('Text-Preparation-Worker Connector', task_queue='Text-Prep-Queue')    
    
    for data in task_queue.listen():
        print("Received the following task from Text-Prep-Queue: ")
        print(data)
        try:
            print("Starting to process received data")
            if "resource_id" in data and "filename" in data and "type" in data:
                report_status_to_API(queue_status=11, status_queue=status_queue, filename=data["resource_id"]+ "/" + data["filename"])

                file_type = data["type"]
                filename = data["filename"]
                resource_id = data["resource_id"]

                return_value = process_file(file_type, filename, resource_id, minio_client)

                # If the task was successfully processed, the if-statement is executed
                # Otherwise, the status queue is updated to: failure
                if return_value[0]:
                    report_status_to_API(queue_status=200, status_queue=status_queue, filename=data["resource_id"]+ "/" + data["filename"])
                else:
                    report_status_to_API(queue_status=12, status_queue=status_queue, filename=data["resource_id"]+ "/" + data["filename"], message=return_value[1])

                if return_value[1]:
                    print("Processing finished successfully")
            else:
                #TODO: Rewrite error message section. Currently deprecated.
                # Received parameters are wrong --> Update status queue and set task processing to: failure
                if "text" not in data and "type" in data:
                    report_status_to_API(queue_status=12, status_queue=status_queue, filename="failure", message="text key is missing or misspelled within the JSON.")
                elif "type" not in data and "text" in data:
                    report_status_to_API(queue_status=12, status_queue=status_queue, filename="failure", message="type key is missing or misspelled within the JSON.")
                else:
                    report_status_to_API(queue_status=12, status_queue=status_queue, filename="failure", message="Both keys are not correct")
        except Exception as e:
            # Received parameters are wrong --> Update status queue and set task processing to: failure
            report_status_to_API(queue_status=12, status_queue=status_queue, filename="failure", message="Data is not valid JSON. Processing cancelled")
            raise e


if __name__ == "__main__":
    print("Text-Prep-Worker is running")
    infinite_loop()
    print("Text-Prep-Worker stops running")
