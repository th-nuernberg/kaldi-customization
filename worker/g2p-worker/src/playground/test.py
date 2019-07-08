import subprocess

f = open("blah.txt", "w")
subprocess.call(["phonetisaurus-train", "-l", "lexicon.txt", "-s2d", "-g", "-o", "8"])
subprocess.call(["phonetisaurus-apply", "--model", "train/model.fst", "--word_list", "voc.tmp", "-n", "2", "-l", "lexicon.txt", "--beam", "10000", "-g", "-t", "10000"], stdout=f)

    