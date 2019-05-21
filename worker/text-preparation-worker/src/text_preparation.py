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


'''
    By calling this function the status queue is updated.
    Possible updates for the status queue are:
        - Pending
        - InProgress
        - Success
        - Warning
        - Failure            
    Before a task is started by the text-preparation-worder, its status
    within the status queue is pending.
    After starting the task, the status of the task changes into InProgress.
    Depending on the outcome of the procession, the status of the task may change into:
        - Success
        - Warning
        - Failure        
'''
def report_status_to_API(queue_status):
    pass


'''
    This function saves the unique word list into the file system as a txt-file.
    The following directory will be used to save the unique world list:
        /text-preparation/out/<model_id>/<id>
'''
def save_textfile(text_list):
    f = open(os.getcwd() + "/out/unique_word_list.txt", "a")
    for sentence in text_list:
        f.write(sentence + "\n")
    f.close()


def retrieve_all_words(text):
    regex = r"[^a-zA-ZäöüÄÖÜß]+"
    all_words = re.split(regex, text)
    return all_words[:-1]


def create_unique_list(word_list):
    unique_list = sorted(list(set(word_list)))
    return unique_list


'''
    The following 5 functions are different kinds of parsers, depending on the given file type.
'''
def pdf_parser(file_path):
    with open(file_path, "rb") as file_handler:
        pdfReader = PyPDF2.PdfFileReader(file_handler)

        # These variables are needed in order to parse the whole PDF-file
        num_pages = pdfReader.numPages
        count = 0
        text = ""

        #The while loop will read each page
        #Important note: Some lines of the PDF-files are read incorect. 
        #TODO: Search for different PDF reader libraries and test whether they achieve better results
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()

        word_list = retrieve_all_words(text)
        unique_list = create_unique_list(word_list)

    return unique_list


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
    unique_list = create_unique_list(word_list)

    return unique_list


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
        unique_list = create_unique_list(word_list)
    
    return unique_list


def text_parser(file_path):    
    with open(file_path, "r") as file_handler:
        text = file_handler.read()

        all_words = retrieve_all_words(text)
        unique_words = create_unique_list(all_words)

    return unique_words


def ocr_parser(file_path):
    # Open image and extract text into pdf
    text = pytesseract.image_to_string(Image.open(file_path), lang="deu")

    # Extracted text is a string. Therefore, it is possible to retrieve all words
    # and after that create the unique_word_list
    word_list = retrieve_all_words(text)
    unique_word_list = create_unique_list(word_list)

    return unique_word_list


'''
    This function is called, in order to open the received filename of the API.
    All files which need to be processed are saved within:
        /text-preparation/in/<project_id>/<model_id>/<id>
'''
def process_file(file_path, file_type):
    '''
        try:
            normal_file_handle = open(file_path, "r", encoding="ISO-8859-1")
            binary_file_handle = open(file_path, "rb")
        except:
            return (False, "File not found within given directory")
    '''
    parsed_text = []

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
        save_textfile(parsed_text)
    except:
        return (False, "Failed to save word list")
    return (True, "Processing of data has finished successfully")


def infinite_loop():
    working_dir = os.getcwd()

    conn = redis.Redis(host='redis', port=6379, db=0, password="kalditproject")
    pubsub = conn.pubsub()
    while True:

        data = conn.blpop('Text-Prep-Queue', 1)        
        if data:
            print("Received the following task from Text-Prep-Queue: ")
            print(data)
            json_data = json.loads(data[1])
            print("Starting to process received data")
            return_value = process_file("/text_prep_worker/in/" + json_data["text"], json_data["type"])
            print(return_value[1])

if __name__ == "__main__":
    print("Text-Prep-Worker is running")
    infinite_loop()
    print("text-Prep-Worker stops running")
