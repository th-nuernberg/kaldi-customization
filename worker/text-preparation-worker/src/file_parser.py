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


def pdf_parser(file_path):
    # Converts all pages of the PDF-file into PNG-files
    print("Starting to transform the received PDF-file into PNG-files")
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(file_path,
                                output_folder=path,
                                dpi=300, fmt=".jpg")

    print("Finished transforming the PDF-file into image-files")

    # Iterates through all images and retrieves the text
    print("Starting to process the image-files with the OCR-scanner")
    full_text = ""
    for image in images:
        print("Starting to process : " + str(image))
        text = pytesseract.image_to_string(image, lang="deu")
        full_text += text + "\n"
        print("Finished finished processing of " + str(image))
        print("--------------------------------------")
    return full_text


def word_parser(file_path):
    # Opens word file properly
    word_doc = docx.Document(file_path)

    # Extract text from file into a list
    full_text = ""
    for para in word_doc.paragraphs:
        full_text += para.text + "\n"

    return full_text


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
        full_text = soup.body.getText()

    return full_text


def text_parser(file_path):
    with open(file_path, "r") as file_handler:
        full_text = file_handler.read()
    return full_text


def ocr_parser(file_path):
    # Open image and extract text into pdf
    full_text = pytesseract.image_to_string(Image.open(file_path), lang="deu")
    return full_text

def generate_corpus(text):
    
    sentences = re.split("[\.|\?|\!]\s", text)
    
    clean_sentences = []
    for sentence in sentences:
        sentence = re.sub(r"[--–—−]\n([a-z])", r"\g<1>", sentence)
        sentence = sentence.lower()

        sentence = re.sub("\n", " ", sentence)
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
        sentence = re.sub(r"[^a-z\s\"]+", " ", sentence)

        clean_sentences.append(sentence)

    return clean_sentences