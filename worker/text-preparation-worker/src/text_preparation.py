# -*- encoding: utf-8 -*-
#!/usr/bin/python
import json
import os

from connector import *
from file_parser import (pdf_parser, html_parser, word_parser,
                         text_parser, ocr_parser, generate_corpus)
from minio_communication import download_from_bucket, upload_to_bucket, does_bucket_exist, minio_buckets


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


def process_file(file_type, resource_uuid, minio_client):
    '''
    This function is called, in order to open the received filename of the API.
    All files which need to be processed are saved within:
        /text-preparation/in/<resource_uuid>/source
    The following file types are supported:
        - PDF
        - Docx
        - HTML
        - txt
        - PNG or JPG
    '''
    text_prep_input = "/text_prep_worker/in/"
    text_prep_output = "/text_prep_worker/out/"
    file_path = text_prep_input + resource_uuid

    # Step 1: Checks whether the requested bucket exist
    existance_result_in = does_bucket_exist(minio_client, minio_buckets["RESOURCE_BUCKET"])
    if not existance_result_in[0]:
        return existance_result_in

    # Step 2: Downloads the needed file which is located within the texts-in bucket
    download_result = download_from_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], resource_uuid + "/source", file_path)
    if not download_result[0]:
        return download_result

    # Step 3: Process the downloaded file
    #         After processing the corpus is ready
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
        corpus_name = resource_uuid + "_corpus"
        save_textfile(corpus, corpus_name)
    except:
        return (False, "Failed to save corpus")

    # Step 5: Upload corpus in bucket
    corpus_path = text_prep_output + corpus_name
    corpus_upload_result = upload_to_bucket(minio_client, minio_buckets["RESOURCE_BUCKET"], resource_uuid + "/corpus.txt", corpus_path)
    if not corpus_upload_result[0]:
        return corpus_upload_result

    # Step 6: Remove local files
    remove_local_files(text_prep_input)
    remove_local_files(text_prep_output)

    return (True, "Processing of data has finished successfully")


def infinite_loop():
    _, task_queue, status_queue, minio_client = parse_args('Text-Preparation-Worker Connector', task_queue='Text-Prep-Queue')

    for data in task_queue.listen():
        print("Received the following task from Text-Prep-Queue: ")
        print(data)

        task = None

        try:
            print("Starting to process received data")
            task = TextPrepTask(**data)

            status_queue.submit(TextPrepStatus(
                id=TextPrepStatusCode.IN_PROGRESS,
                resource_uuid=task.resource_uuid,
                message="Task in progress"))
            return_value = process_file(task.file_type, task.resource_uuid, minio_client)

            # If the task was successfully processed, the if-statement is executed
            # Otherwise, the status queue is updated to: failure
            if return_value[0]:
                status_queue.submit(TextPrepStatus(
                    id=TextPrepStatusCode.SUCCESS,
                    resource_uuid=task.resource_uuid,
                    message="Task finished successfully"
                ))
            else:
                status_queue.submit(TextPrepStatus(
                    id=TextPrepStatusCode.FAILURE,
                    resource_uuid=task.resource_uuid,
                    message="Task has failed"
                ))

            if return_value[1]:
                print("Processing finished successfully")
        except Exception as e:
            status_queue.submit(TextPrepStatus(
                id=TextPrepStatusCode.FAILURE,
                resource_uuid=task.resource_uuid if task else None,
                message=str(e)
            ))
            raise e


if __name__ == "__main__":
    print("Text-Prep-Worker is running")
    infinite_loop()
    print("Text-Prep-Worker stops running")
