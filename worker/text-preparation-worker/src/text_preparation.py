# -*- encoding: utf-8 -*-
import os
import re
import redis
import PyPDF2 
import docx
import json
from bs4 import BeautifulSoup, Comment

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


def report_status_to_API(queue_status, conn, file_path=None):
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
    if queue_status == 11:
        message = "Task in progress"
    elif queue_status == 12:
        message == "Task has failed"
    elif queue_status == 200:
        message = "Task finished successfully"

    # If the task was processed successfully, this statement is called.
    # Otherwise the user will be notified, that something went wrong.
    if queue_status == 200:
        conn.publish('Status-Queue', json.dumps({
        "type": "text-prep",
        "text": file_path,
        "status": queue_status,
        "msg": message
        }))
    else:
        # TODO: If task has failed, add a reason why.
        conn.publish('Status-Queue', json.dumps({
        "type": "text-prep",
        "status": queue_status,
        "msg": message   
        }))

def save_textfile(text_list, filename):
    '''
    This function saves the unique word list into the file system as a txt-file.
    The following directory will be used to save the unique world list:
        /text-preparation/out/<filename>.txt
    '''

    f = open("/text_prep_worker/out/" + filename, "w")
    for sentence in text_list:
        f.write(sentence + "\n")
    f.close()


def retrieve_all_words(text):
    remove_newline_after_minus = re.sub("[--–—−]\n[a-z]+", "", text)
    regex = r"[^a-zA-ZäöüÄÖÜß]+"
    all_words = re.split(regex, remove_newline_after_minus)
    return all_words


def create_unique_list(word_list):
    unique_word_list = sorted(list(set(word_list)))
    return unique_word_list


def pdf_parser(file_path):
    # Converts all pages of the PDF-file into PNG-files
    print("Starting to transform the received PDF-file into PNG-files")
    images = convert_from_path(file_path,
                               dpi=300, fmt=".png")
    print("Finished transforming the PDF-file into PNG-files")

    # Iterates through all images and retrieves the word list
    print("Starting to process the PNG-files with the OCR-scanner")
    complete_word_list = []
    for image in images:        

        print("Starting to process : " + str(image))
        text = pytesseract.image_to_string(image, lang="deu")
        print("Finished retrieving text from " + str(image))

        print("Starting to create the word_list for the text")
        word_list = retrieve_all_words(text)
        print("Finished finished processing of " + str(image))

        for word in word_list:
            complete_word_list.append(word)
        print("--------------------------------------")

    # After retrieving all words, the unique word list is created
    print("Creating unique word list")
    unique_word_list = create_unique_list(complete_word_list)

    return unique_word_list


def word_parser(file_path):
    # Opens word file properly
    word_doc = docx.Document(file_path)
    
    # Extract text from file into a list
    fullText = []    
    for para in word_doc.paragraphs:
        fullText.append(para.text)
    
    # Create the word list and the unique list
    word_list = []
    for paragraph in fullText:
        words = retrieve_all_words(paragraph)
        for word in words:
            word_list.append(word)
    unique_word_list = create_unique_list(word_list)

    return unique_word_list


def html_parser(file_path):
    with open(file_path, "r", encoding="ISO-8859-1") as file_handler:
        # Blacklisted tags which will be ignored and extracted from the HTML-files
        blacklist = ["script", "style"]
        soup = BeautifulSoup(file_handler.read(), features="html.parser")
        # Strips all blacklisted HTML-tags

        for tag in soup.findAll():
            if tag.name.lower() in blacklist:
                tag.extract()

        # Retrieves all comments from the HTML-file and removes them

        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # Retrieves the visible text of the web page
        webpage_text = soup.body.getText()

        word_list = retrieve_all_words(webpage_text)
        unique_word_list = create_unique_list(word_list)
    
    return unique_word_list


def text_parser(file_path):    
    with open(file_path, "r") as file_handler:
        text = file_handler.read()

        all_words = retrieve_all_words(text)
        unique_word_list = create_unique_list(all_words)

    return unique_word_list


def ocr_parser(file_path):
    # Open image and extract text into pdf
    text = pytesseract.image_to_string(Image.open(file_path), lang="deu")

    # Extracted text is a string. Therefore, it is possible to retrieve all words
    # and after that create the unique_word_list
    word_list = retrieve_all_words(text)
    unique_word_list = create_unique_list(word_list)

    return unique_word_list


def process_file(file_type, filename):
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
    file_path = "/text_prep_worker/in/" + filename

    try:
        if file_type == "pdf":
            parsed_text = pdf_parser(file_path)
        elif file_type == "docx":
            parsed_text = word_parser(file_path)
        elif file_type == "html":
            parsed_text = html_parser(file_path)
        elif file_type == "txt":
            parsed_text = text_parser(file_path)
        elif file_type == "png" or file_type == "jpg":
            parsed_text = ocr_parser(file_path)
        else:        
            return (False, "Given file type is not supported. Finishing processing")
    except Exception as e:
        print(e)
        return (False, "Failed to parse given file")

    try:
        save_textfile(parsed_text, filename)
    except:
        return (False, "Failed to save word list")
    return (True, "Processing of data has finished successfully")


def infinite_loop():
    conn = redis.Redis(host='redis', port=6379, db=0, password="kalditproject")
    while True:

        data = conn.blpop('Text-Prep-Queue', 1)      
        if data:
            print("Received the following task from Text-Prep-Queue: ")
            print(data)
            try:
                json_data = json.loads(data[1])
                print("Starting to process received data")
                if "text" in json_data and "type" in json_data:
                    return_value = process_file(json_data["type"], json_data["text"])    

                    # If the task was successfully processed, the if-statement is executed
                    # Otherwise, the status queue is updated to: failure
                    if return_value[0]:
                        file_path = "/text_prep_worker/out/" + json_data["type"]
                        report_status_to_API(queue_status=200, conn=conn, file_path=file_path)
                    else:
                        report_status_to_API(queue_status=12, conn=conn)
                    
                    print(return_value[1])
                else:
                    if "text" not in json_data and "type" in json_data:
                        print("text key is missing or misspelled within the JSON.")
                    elif "type" not in json_data and "text" in json_data:
                        print("type key is missing or misspelled within the JSON.")
                    else:
                        print("Both keys are not correct")
                    # Received parameters are wrong --> Update status queue and set task processing to: failure
                    report_status_to_API(queue_status=12, conn=conn)
            except:
                print("Data is not valid JSON. Processing cancelled")
                # Received parameters are wrong --> Update status queue and set task processing to: failure
                report_status_to_API(queue_status=12, conn=conn)
            

if __name__ == "__main__":
    print("Text-Prep-Worker is running")
    infinite_loop()    
    print("text-Prep-Worker stops running")
