import re
import subprocess


def execute_phonetisaurus(lexicon, word_list):
    subprocess.call(["phonetisaurus-train", "-l", "/g2p_worker/in/" + lexicon, "-s2d", "-g", "-o", "8"])
    
    # Write the new file into the out directory of the g2p_worker
    with open("/g2p_worker/out/" + word_list, "w") as file_handler:            
        # Applies the previously trained graph onto the wordlist and creates phones for all words
        # Phone list is saved within /g2p_worker/out/
        subprocess.call(["phonetisaurus-apply", "--model", "train/model.fst", "--word_list", "/g2p_worker/in/" + word_list, "-n", "2", "-l", lexicon, "--beam", "10000", "-g", "-t", "10000"], stdout=file_handler)

    # Moves the created graph into /g2p_worker/out/
    subprocess.call(["mv", "train/model.fst", "/g2p_worker/out/model.fst"])


#TODO: Save the final word list within the correct directory
def merge_word_lists(unique_words):
    '''
    This function merges multiple word lists into one.

    Note: Due to the fact that multiple files are merged, it is possible that multiple files
    use the same words. The final word list is an unique list. Therefore, all words occur only
    once. In order to achieve this behavior, the lists are converted into sets and these sets 
    are combined.
    '''
    first_list = open(unique_words[0], "r").read().lower()
    first_word_list = re.split("\n", first_list)

    for wl in range(1, len(unique_words), 1):
        second_list = open(unique_words[wl], "r").read().lower()
        second_word_list = re.split("\n", second_list)
        first_word_list = set(first_word_list).union(set(second_word_list))
    
    first_word_list = sorted(first_word_list)
    first_word_list.remove("")
    
    with open("final_word_list.txt", "w") as file_writer:
        for word in first_word_list:
            file_writer.write(word + "\n")


#TODO: Save the final corpus within the correct directory
def merge_corpuses(corpus_list):
    '''
    This function merges multiple corpuses into one file. In order to do so, the first corpus of 
    the list is extended with the remaining ones. 

    One assumption for this function is, that it does not matter whether a sentence occurs 
    multiple times. Every sentence is appended.

    The final corpus is locally saved and afterwards uploaded into the corresponding MinIO-Bucket
    '''
    first_corpus = open(corpus_list[0], "r").read()
    first_corpus_list = re.split("\n", first_corpus)    

    for corpus in range(1, len(corpus_list), 1):
        second_corpus = open(corpus_list[corpus], "r").read()
        second_corpus_list = re.split("\n", second_corpus)

        # Appends the sentences of the second corpus to the first one
        for sentence in second_corpus_list:
            first_corpus_list.append(sentence)    

    with open("final_corpus.txt", "w") as file_writer:
        for sentence in first_corpus_list:
            if sentence != "":
                file_writer.write(sentence + "\n")


#merge_word_lists(["playground/voc.tmp", "playground/blah.txt", "playground/gamestar", "playground/kafka", "playground/test"])
#merge_corpuses(["playground/kafka_corpus", "playground/second_corpus", "playground/test"])