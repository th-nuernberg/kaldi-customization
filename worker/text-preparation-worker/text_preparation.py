# -*- encoding: utf-8 -*-
import os
import re
import PyPDF2 
import docx
from bs4 import BeautifulSoup, Comment


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
    This function saves the extracted text into a temp-file.
    The created temp-file will be processed afterwards
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
def xml_parser(file_handler):
    #TODO: Check whether this function is really necessary for us.
    raise NotImplementedError("Function is currently not implemented")


def pdf_parser(binary_file_handle):
    pdfReader = PyPDF2.PdfFileReader(binary_file_handle)

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


def html_parser(file_handler):
    # remove these tags, complete with contents.
    blacklist = ["script", "style"]

    soup = BeautifulSoup(file_handler, features="html.parser")

    # Strips all blacklisted HTML-tags
    for tag in soup.findAll():
        if tag.name.lower() in blacklist:
            tag.extract()

    # Strips all HTML-comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Retrieves the visible text of the web page
    webpage_text = soup.body.getText().encode("utf8")
    
    word_list = retrieve_all_words(webpage_text)
    unique_list = create_unique_list(word_list)
    
    return unique_list


def text_parser(file_handler):
    text = file_handler.read()

    all_words = retrieve_all_words(text)
    unique_words = create_unique_list(all_words)

    return unique_words


'''
    This function is called, in order to open the received filename of the API.
    All files which need to be processed will be stored within:
        /text-preparation/in/<model_id>/<id>
'''
def process_file(file_path):

    try:
        normal_file_handle = open(file_path, "r")
        binary_file_handle = open(file_path, "rb")
    except:
        raise NotImplementedError("File could not be opened, because it could not be located within the working directory")

    parsed_text = []

    if file_path.endswith(".pdf"):
        parsed_text = pdf_parser(binary_file_handle)
    elif file_path.endswith(".docx"):
        parsed_text = word_parser(file_path)
    elif file_path.endswith(".html"):
        parsed_text = html_parser(normal_file_handle)
    elif file_path.endswith(".txt"):
        parsed_text = text_parser(normal_file_handle)
    elif file_path.endswith(".xml"):
        parsed_text = xml_parser(normal_file_handle)
    else:
        print("Given file is not supported. Finishing processing")
        exit(1)

    save_textfile(parsed_text)    


working_dir = os.getcwd()
# Testing text-files
# process_file(working_dir + "/test-files/txt/kafka.txt")
# process_file(working_dir + "/test-files/txt/text_generator.txt")

# Testing HTML-files
# process_file(working_dir + "/test-files/html/hein.html")
# process_file(working_dir + "/test-files/html/hochschule.html")
# process_file(working_dir + "/test-files/html/gamestar.html")

# Testing PDF-files
# process_file(working_dir + "/test-files/pdf/kafka.pdf")
# process_file(working_dir + "/test-files/pdf/text_generator.pdf")

# Testing Word-files
# process_file(working_dir + "/test-files/word/kafka.docx")
# process_file(working_dir + "/test-files/word/text_generator.docx")