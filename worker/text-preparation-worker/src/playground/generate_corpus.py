import os 
import re

clean_sentences = []
with open("../test-files/txt/kafka.txt", "r") as file_handler:
    text = file_handler.read()
    sentences = re.split("[\.|\?|\!]\s", text)
    
    for sentence in sentences:
        sentence = sentence.lower()

        sentence = re.sub("\n", "", sentence)
        # sentence = re.sub("ä", "ae", sentence)
        # sentence = re.sub("ö", "oe", sentence)
        # sentence = re.sub("ü", "ue", sentence)
        sentence = re.sub("1", "eins ", sentence)
        sentence = re.sub("2", "zwei ", sentence)
        sentence = re.sub("3", "drei ", sentence)
        sentence = re.sub("4", "vier ", sentence)
        sentence = re.sub("5", "fuenf ", sentence)
        sentence = re.sub("6", "sechs ", sentence)
        sentence = re.sub("7", "sieben ", sentence)
        sentence = re.sub("8", "acht ", sentence)
        sentence = re.sub("9", "neun ", sentence)
        sentence = re.sub(r"[^a-zäöüß\s]+", "", sentence)

        clean_sentences.append(sentence)

with open("test", "w") as file_handler:
    for sentence in clean_sentences:
        file_handler.write(sentence + "\n")
