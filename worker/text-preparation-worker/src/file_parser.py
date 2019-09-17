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


def pdf_parser(file_path, log_file_handler):
    log_file_handler.write("Starting to transform the received PDF-file into PNG-files \n")

    # Converts all pages of the PDF-file into PNG-files
    print("Starting to transform the received PDF-file into PNG-files")
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(file_path,
                                output_folder=path,
                                dpi=300, fmt=".jpg")

    print("Finished transforming the PDF-file into image-files")
    log_file_handler.write("Finished transforming the PDF-file into image-files \n")

    # Iterates through all images and retrieves the text
    print("Starting to process the image-files with the OCR-scanner")
    log_file_handler.write("Starting to process the image-files with the OCR-scanner \n")
    full_text = ""
    for image in images:
        print("Starting to process: {}".format(image))
        log_file_handler.write("Starting to process: {} \n".format(image))

        text = pytesseract.image_to_string(image, lang="deu")
        full_text += text + "\n"

        log_file_handler.write("Finished finished processing of {} \n".format(image))
        log_file_handler.write("------------------------------------------------ \n")
        print("Finished finished processing of {}".format(image))
        print("--------------------------------------")
    return full_text


def word_parser(file_path, log_file_handler):
    print("Starting to extract the text out of the received docx-file")
    log_file_handler.write("Starting to extract the text out of the received docx-file \n")
    
    # Opens word file properly
    word_doc = docx.Document(file_path)
    # Extract text from file into a list
    full_text = ""
    for para in word_doc.paragraphs:
        full_text += para.text + "\n"

    print("The parsing process of the docx-file finished")
    log_file_handler.write("The parsing process of the docx-file finished \n")
    return full_text


def html_parser(file_path, log_file_handler):
    print("Starting to extract the text out of the received html-file")
    log_file_handler.write("Starting to extract the text out of the received html-file \n")

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
        full_text = soup.body.getText()

    print("The parsing process of the html-file finished")
    log_file_handler.write("The parsing process of the html-file finished \n")

    return full_text


def text_parser(file_path, log_file_handler):
    print("Starting to extract the text out of the received txt-file")
    log_file_handler.write("Starting to extract the text out of the received txt-file \n")

    with open(file_path, "r") as file_handler:
        full_text = file_handler.read()

    print("The parsing process of the txt-file finished")
    log_file_handler.write("The parsing process of the txt-file finished \n")

    return full_text


def ocr_parser(file_path, log_file_handler):
    print("Starting to extract the text out of the received image")
    log_file_handler.write("Starting to extract the text out of the received image \n")

    # Open image and extract text into pdf
    full_text = pytesseract.image_to_string(Image.open(file_path), lang="deu")

    print("The parsing process of the image finished")
    log_file_handler.write("The parsing process of the image finished \n")

    return full_text

def generate_corpus(text):
    sentences = re.split(r"[\.|\?|\!]\s", text)

    clean_sentences = []
    for sentence in sentences:
        sentence = re.sub(r"[--–—−]\n([a-z])", r"\g<1>", sentence)
        sentence = sentence.lower()

        sentence = re.sub(r"[^a-z\s0-9äöü]+", " ", sentence)
        sentence = re.sub(r"\n", " ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"ä", "\"a", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"ö", "\"o", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"ü", "\"u", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"ß", "\"s", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"0", "null ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"1", "eins ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"2", "zwei ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"3", "drei ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"4", "vier ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"5", "fuenf ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"6", "sechs ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"7", "sieben ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"8", "acht ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"9", "neun ", sentence, flags=re.MULTILINE)
        sentence = re.sub(r"\s+", " ", sentence, flags=re.MULTILINE)
        

        clean_sentences.append(sentence)

    return clean_sentences