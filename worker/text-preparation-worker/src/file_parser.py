# -*- encoding: utf-8 -*-
import docx
import PyPDF2
import re
import tempfile
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
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(file_path,
                                output_folder=path,
                                dpi=300, fmt=".jpg")

    print("Finished transforming the PDF-file into image-files")

    # Iterates through all images and retrieves the word list
    print("Starting to process the image-files with the OCR-scanner")
    complete_word_list = []
    full_text = ""
    for image in images:
        print("Starting to process : " + str(image))
        text = pytesseract.image_to_string(image, lang="deu")
        full_text = full_text + text + "\n"
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

    return unique_word_list, full_text


def word_parser(file_path):
    # Opens word file properly
    word_doc = docx.Document(file_path)

    # Extract text from file into a list
    text = ""
    fullText = []
    for para in word_doc.paragraphs:
        fullText.append(para.text)
        text = text + para + "\n"

    # Create the word list and the unique list
    word_list = []
    for paragraph in fullText:
        words = retrieve_all_words(paragraph)
        for word in words:
            word_list.append(word)
    unique_word_list = create_unique_list(word_list)

    return unique_word_list, text


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

    return unique_word_list, webpage_text


def text_parser(file_path):
    with open(file_path, "r") as file_handler:
        text = file_handler.read()

        all_words = retrieve_all_words(text)
        unique_word_list = create_unique_list(all_words)

    return unique_word_list, text


def ocr_parser(file_path):
    # Open image and extract text into pdf
    text = pytesseract.image_to_string(Image.open(file_path), lang="deu")

    # Extracted text is a string. Therefore, it is possible to retrieve all words
    # and after that create the unique_word_list
    word_list = retrieve_all_words(text)
    unique_word_list = create_unique_list(word_list)

    return unique_word_list, text

def generate_corpus(text):
    
    sentences = re.split("[\.|\?|\!]\s", text)
    
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.lower()

        sentence = re.sub("\n", "", sentence)
        sentence = re.sub("ä", "\"a", sentence)
        sentence = re.sub("ö", "\"o", sentence)
        sentence = re.sub("ü", "\"u", sentence)
        sentence = re.sub("ß", "\"s", sentence)
        sentence = re.sub("1", "eins ", sentence)
        sentence = re.sub("2", "zwei ", sentence)
        sentence = re.sub("3", "drei ", sentence)
        sentence = re.sub("4", "vier ", sentence)
        sentence = re.sub("5", "fuenf ", sentence)
        sentence = re.sub("6", "sechs ", sentence)
        sentence = re.sub("7", "sieben ", sentence)
        sentence = re.sub("8", "acht ", sentence)
        sentence = re.sub("9", "neun ", sentence)
        sentence = re.sub(r"[^a-z\s]+", "", sentence)

        clean_sentences.append(sentence)

    return clean_sentences