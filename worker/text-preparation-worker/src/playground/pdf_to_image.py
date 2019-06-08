from pdf2image import convert_from_path, convert_from_bytes

import re

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


def save_textfile(text_list, filename):
    f = open(filename, "w")
    for sentence in text_list:
        f.write(sentence + "\n")
    f.close()


def retrieve_all_words(text):
    regex = r"[^a-zA-ZäöüÄÖÜß]+"
    all_words = re.split(regex, text)
    return all_words


def create_unique_list(word_list):
    unique_list = sorted(list(set(word_list)))
    return unique_list


# Converts all pages of the PDF-file into PNG-files
print("Starting to transform the received PDF-file into PNG-files")
images = convert_from_path('../test-files/pdf/kafka.pdf',
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

# After retrieving all words, the unique word list is created
print("Creating unique word list")
unique_word_list = create_unique_list(complete_word_list)
print("Saving unique_word_list into dfs")
save_textfile(unique_word_list, "betterKafka")







    ''' TODO: New goal is to process the received PDF-files in a different way
        1) Use the PyPDF2 library to open the PDF-file
        2) Convert the PDF into images
        3) Extract the text within the images by using Google's PyTesseract OCR scan                
    '''
    with open(file_path, "rb") as file_handler:
        pdfReader = PyPDF2.PdfFileReader(file_handler)

        # These variables are needed in order to parse the whole PDF-file
        num_pages = pdfReader.numPages
        count = 0
        text = ""

        # The while loop will read each page                
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        word_list = retrieve_all_words(text)
        unique_list = create_unique_list(word_list)

    return unique_list

