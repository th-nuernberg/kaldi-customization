import os
import re
import subprocess


def execute_phonetisaurus(lexicon):
    '''
    This function executes two Phonetisaurus commands:
        1) phonetisaurus-train
        2) phonetisaurus-apply
    These calls are used to create a word list with all their phones. 

    This function saves two files:
        1) model.fst --> This file is a graph which was created with the phonetisaurus-train command
        2) word list with phones --> This file consists of all words and their phones
    All these files are saved locally and are afterwards uploaded to their corresponding MinIO-Bucket

    Loading lexicon from: /data_prep_worker/in/
    Loading final_word_list from: /data/prep_worker/out/
    Saving all files to: /data_prep_worker/out/
    '''
    # Trains a new graph with the base lexicon
    subprocess.call(["phonetisaurus-train", "-l", "/data_prep_worker/in/" + lexicon, "-s2d", "-g", "-o", "8"])
    
    with open("/data_prep_worker/out/final_word_list_with_phones", "w") as file_handler:            
        # Applies the previously trained graph onto the word list and creates phones for all words
        subprocess.call(["phonetisaurus-apply", "--model", "train/model.fst", "--word_list", "/data_prep_worker/out/final_word_list", "-n", "2", "-l", lexicon, "--beam", "10000", "-g", "-t", "10000"], stdout=file_handler)

    # Moves the created graph into /data_prep_worker/out/
    subprocess.call(["mv", "train/model.fst", "/data_prep_worker/out/model.fst"])


def merge_word_lists(unique_words):
    '''
    This function merges multiple word lists into one.

    Note: Due to the fact that multiple files are merged, it is possible that multiple files
    use the same words. The final word list is an unique list. Therefore, all words occur only
    once. In order to achieve this behavior, the lists are converted into sets and these sets 
    are combined.

    The final word list is locally saved and afterwards uploaded into the corresponding MinIO-Bucket

    Loading all files from: /data_prep_worker/in/
    Saving final word list into: /data_prep_worker/out/
    '''
    first_list = open("/data_prep_worker/in/" + unique_words[0], "r").read().lower()
    first_word_list = re.split("\n", first_list)

    for word_list in range(1, len(unique_words), 1):
        second_list = open("/data_prep_worker/in/" + unique_words[word_list], "r").read().lower()
        second_word_list = re.split("\n", second_list)
        first_word_list = set(first_word_list).union(set(second_word_list))

    first_word_list = sorted(first_word_list)
    first_word_list.remove("")

    with open("/data_prep_worker/out/final_word_list", "w") as file_writer:
        for word in first_word_list:
            file_writer.write(word + "\n")


def merge_corpus_list(corpus_list):
    '''
    This function merges multiple corpuses into one file. In order to do so, the first corpus of 
    the list is extended with the remaining ones. 

    One assumption for this function is, that it does not matter whether a sentence occurs 
    multiple times. Every sentence is appended.

    The final corpus is locally saved and afterwards uploaded into the corresponding MinIO-Bucket

    Loading all files from: /data_prep_worker/in/
    Saving merged corpus into: /data_prep_worker/out/
    '''
    first_corpus = open("/data_prep_worker/in/" + corpus_list[0], "r").read()
    first_corpus_list = re.split("\n", first_corpus)    

    for corpus in range(1, len(corpus_list), 1):
        second_corpus = open("/data_prep_worker/in/" + corpus_list[corpus], "r").read()
        second_corpus_list = re.split("\n", second_corpus)

        # Appends all sentences of the second corpus to the first one
        for sentence in second_corpus_list:
            first_corpus_list.append(sentence)

    with open("/data_prep_worker/out/final_corpus", "w") as file_writer:
        for sentence in first_corpus_list:
            if sentence != "":
                file_writer.write(sentence + "\n")


def remove_local_files(path):
    '''
    This function removes all files which were created within the 
    /data_prep_worker/in/ and 
    /data_prep_worker/out/ directories.
    '''
    files = os.listdir(path)
    for file in files:
        os.remove(path + file)
