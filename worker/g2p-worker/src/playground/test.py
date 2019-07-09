import re
import subprocess

def merge_sets(unique_words):
    first_list = open(unique_words[0], "r").read().lower()
    first_word_list = re.split("\n", first_list)

    for wl in range(1, len(unique_words), 1):
        second_list = open(unique_words[wl], "r").read().lower()
        second_word_list = re.split("\n", second_list)
        first_word_list = set(first_word_list).union(set(second_word_list))
    
    first_word_list = sorted(first_word_list)
    first_word_list.remove("")
    print(first_word_list)    


def execute_phonetisaurus(lexicon, word_list):
    subprocess.call(["phonetisaurus-train", "-l", lexicon, "-s2d", "-g", "-o", "8"])
    
    # Write the new file into the out directory of the g2p_worker
    with open(word_list + "_done", "w") as file_handler:            
        # Applies the previously trained graph onto the wordlist
        subprocess.call(["phonetisaurus-apply", "--model", "train/model.fst", "--word_list", word_list, "-n", "2", "-l", lexicon, "--beam", "10000", "-g", "-t", "10000"], stdout=file_handler)

    # Moves the created graph into the out directory of the g2p_worker
    subprocess.call(["mv", "train/model.fst", "/g2p_worker/out/model.fst"])


#merge_sets(["voc.tmp", "blah.txt", "gamestar", "kafka", "test"])

#execute_phonetisaurus("lexicon.txt", "voc.tmp")