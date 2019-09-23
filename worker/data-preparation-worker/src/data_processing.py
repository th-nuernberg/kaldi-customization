# -*- encoding: utf-8 -*-
import os
import re
import subprocess


def execute_phonetisaurus():
    '''
    This function executes the phonetisaurus-apply command
    This call is used to create a lexicon.txt file which is afterwards used by the kaldi-worker

    This function saves one file:
        - lexicon.txt --> This file consists of all words and their phones
    This file is saved locally and are afterwards uploaded to its corresponding MinIO-Bucket

    Loading g2p graph for command from: /data_prep_worker/in/
    Loading final_word_list from: /data/prep_worker/out/
    Saving lexicon.txt in: /data_prep_worker/out/
    '''
    with open("/data_prep_worker/out/lexicon.txt", "w") as file_handler:            
        # Applies the previously trained graph onto the word list and creates phones for all words
        subprocess.call(["phonetisaurus-apply", "--model", "/data_prep_worker/in/g2p_model.fst", "--word_list", "/data_prep_worker/out/final_word_list", 
                         "--beam", "10000", "-g", "-t", "10000"], stdout=file_handler)


def save_txt_file(file_path, content_list):
    '''
    This function saves a given txt-file into the /data_prep_worker/out/ directory.
    '''
    with open(file_path, "w") as file_writer:
        for item in content_list:
            if item != "":
                file_writer.write(item + "\n")


def create_unique_word_list(file_path):
    with open(file_path, "r") as file_handler:
        text = file_handler.read()

        all_words = text.split()
        unique_word_list = sorted(list(set(all_words)))
        if "\xc2\xa0" in unique_word_list:
            unique_word_list.remove("\xc2\xa0")

    return unique_word_list


def merge_corpus_list(corpus_list, log_file_handler):
    '''
    This function merges multiple corpus-files into one file. In order to do so, the first corpus of 
    the list is extended with the remaining ones. 

    It does not matter whether a sentence occurs multiple times. Every sentence is appended.

    Input of this function: list of all corpus-files for this task
    Output of this function: list of all sentences of all corpus-files --> merged corpus list

    Loading all files from: /data_prep_worker/in/
    Saving merged corpus into: /data_prep_worker/out/
    '''
    first_corpus = open(corpus_list[0], "r").read()
    return_corpus_list = re.split("\n", first_corpus)  

    if len(corpus_list) > 1:
        print("Corpus list contains more than one element. Merge process is starting.")
        log_file_handler.write("Corpus list contains more than one element. Merge process is starting. \n")

        for corpus in range(1, len(corpus_list), 1):
            second_corpus = open(corpus_list[corpus], "r").read()
            second_corpus_list = re.split("\n", second_corpus)

            # Appends all sentences of the second corpus to the first one
            for sentence in second_corpus_list:
                if sentence != " " or sentence != "":
                    return_corpus_list.append(sentence)
        return return_corpus_list
    print("There is only one element within the given corpus list. Therefore no merge was needed.")
    log_file_handler.write("There is only one element within the given corpus list. Therefore no merge was needed. \n")
    return return_corpus_list



def remove_local_files(path):
    '''
    This function removes all files which were created within the 
    /data_prep_worker/in/ and 
    /data_prep_worker/out/ directories.
    '''
    files = os.listdir(path)
    for file in files:
        os.remove(path + file)
