# -*- encoding: utf-8 -*-
import json
import os
import redis
from minio import Minio
from minio import ResponseError

from file_parser import pdf_parser, html_parser, word_parser
from file_parser import text_parser, ocr_parser, generate_corpus
from minio_communication import download_from_bucket, upload_to_bucket

def report_status_to_API(queue_status, conn, filename=None, message=None):
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

    conn.publish('Status-Queue', json.dumps({
                 "type": "text-prep",
                 "text": filename,
                 "status": queue_status,
                 "msg": message
                 }))


def save_textfile(text_list, filename):
    '''
    This function saves the unique word list into the file system as a txt-file
    The following directory will be used to save the unique world list:
        /text-preparation/out/<filename>.txt
    '''

    file_handler = open("/text_prep_worker/out/" + filename, "w")
    for sentence in text_list:
        file_handler.write(sentence + "\n")
    file_handler.close()


def process_file(file_type, filename, minio_client):
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
    parsed_text = []
    # Checks whether the requested bucket exists
    try:
        print(minio_client.bucket_exists("texts-in"))
    except ResponseError as err:
        print(err)
        return (False, err)

    # Get a full object and prints the original object stat information.
    download_result = download_from_bucket(minio_client, 'texts-in', filename, 'text_prep_worker/in/')
    if not download_result[0]:
        return download_result

    # Starts to process the downloaded file
    file_path = "/text_prep_worker/in/" + filename
    full_text = ""
    try:
        if file_type == "pdf":
            parsed_text, full_text = pdf_parser(file_path)
        elif file_type == "docx":
            parsed_text, full_text = word_parser(file_path)
        elif file_type == "html":
            parsed_text, full_text = html_parser(file_path)
        elif file_type == "txt":
            parsed_text, full_text = text_parser(file_path)
        elif file_type == "png" or file_type == "jpg":
            parsed_text, full_text = ocr_parser(file_path)            
        else:
            return (False, "Given file type is not supported. Finishing processing")

        # Generates the corpus
        corpus = generate_corpus(full_text)

    except Exception as e:
        print(e)
        return (False, "Failed to parse given file")

    try:
        corpus_name = filename + "_corpus"
        save_textfile(parsed_text, filename)
        save_textfile(corpus, corpus_name)
    except:
        return (False, "Failed to save word list")

    # Saves the created unique word list
    file_path = "/text_prep_worker/out/" + filename
    file_upload_result = upload_to_bucket(minio_client, "texts-out", filename, file_path)
    if not file_upload_result[0]:
        return file_upload_result

    # Saves the created corpus
    corpus_path = "/text_prep_worker/out/" + corpus_name
    corpus_upload_result = upload_to_bucket(minio_client, "texts-out", corpus_name, corpus_path)
    if not corpus_upload_result[0]:
        return corpus_upload_result

    return (True, "Processing of data has finished successfully")


def infinite_loop():
    conn = redis.Redis(host='redis', port=6379, db=0, password="kalditproject")
    minio_client = Minio('minio:9000',
                         access_key='AKIAIOSFODNN7EXAMPLE',
                         secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                         secure=False)

    while True:

        data = conn.blpop('Text-Prep-Queue', 1)
        if data:
            print("Received the following task from Text-Prep-Queue: ")
            print(data)
            try:
                json_data = json.loads(data[1])
                print("Starting to process received data")
                if "text" in json_data and "type" in json_data:
                    report_status_to_API(queue_status=11, conn=conn, filename=json_data["text"])

                    return_value = process_file(json_data["type"], json_data["text"], minio_client)

                    # If the task was successfully processed, the if-statement is executed
                    # Otherwise, the status queue is updated to: failure
                    if return_value[0]:
                        report_status_to_API(queue_status=200, conn=conn, filename=json_data["text"])
                    else:
                        report_status_to_API(queue_status=12, conn=conn, filename=json_data["text"], message=return_value[1])

                    if return_value[1]:
                        print("Processing finished successfully")
                else:
                    # Received parameters are wrong --> Update status queue and set task processing to: failure
                    if "text" not in json_data and "type" in json_data:
                        report_status_to_API(queue_status=12, conn=conn, filename="failure", message="text key is missing or misspelled within the JSON.")
                    elif "type" not in json_data and "text" in json_data:
                        report_status_to_API(queue_status=12, conn=conn, filename="failure", message="type key is missing or misspelled within the JSON.")
                    else:
                        report_status_to_API(queue_status=12, conn=conn, filename="failure", message="Both keys are not correct")
            except Exception as e:
                # Received parameters are wrong --> Update status queue and set task processing to: failure
                report_status_to_API(queue_status=12, conn=conn, filename="failure", message="Data is not valid JSON. Processing cancelled")
                raise e


if __name__ == "__main__":
    print("Text-Prep-Worker is running")
    infinite_loop()
    print("Text-Prep-Worker stops running")
