import os
import sys
import shutil
import re
from collections import namedtuple

if(len(sys.argv) != 2):
	print("Usage: python3 splice_data.py <target_dir>")
	exit()

target_dir = sys.argv[1]

os.mkdir("data")

shutil.copytree(os.path.join(target_dir,"local"),"data/local")

#LOAD SPEAKER DATA
SpeakerPrefab = namedtuple("SpeakerPrefab",["name","gender","utterances"])

speakers = dict()
with open(os.path.join(target_dir,"etc","spk2gender")) as f:
    for line in f:
        x = line.split()
        speakers[x[0]] = SpeakerPrefab(name=x[0],gender=x[1],utterances = list())

utt2spk = list()
with open(os.path.join(target_dir,"etc","utt2spk")) as f:
    for line in f:
        x = line.split()
        speakers[x[1]].utterances.append(x[0])

speaker_list = sorted(speakers.values(),key = lambda v: len(v.utterances))

test_speakers = ["1337ad","BRwgt"]

mono_thresh = 2000
tri1_thresh = 6000
tri2_thresh = 20000

test_spk = [x for x in speaker_list if x.name in test_speakers]
mono_spk = list()
tri1_spk = list()
tri2_spk = list()
tri3_spk = [x for x in speaker_list if x.name not in test_speakers]

for s in [x for x in speaker_list if x.name not in test_speakers]:
    if mono_thresh < 0: break
    mono_spk.append(s)
    mono_thresh -= len(s.utterances)

for s in [x for x in speaker_list if x.name not in test_speakers]:
    if tri1_thresh < 0: break
    tri1_spk.append(s)
    tri1_thresh -= len(s.utterances)

for s in [x for x in speaker_list if x.name not in test_speakers]:
    if tri2_thresh < 0: break
    tri2_spk.append(s)
    tri2_thresh -= len(s.utterances)

# LOAD TEXT TRANSLATION

text = dict()

with open(os.path.join(target_dir,"etc","text")) as f:
	for line in f:
		x = line.split()
		text[x[0]] = " ".join(x[1:])

# LOAD File Location

scp = dict()

with open(os.path.join(target_dir,"etc","wav.scp")) as f:
	for line in f:
		x = line.split()
		scp[x[0]] = " ".join(x[1:])

# METHOD

def create_subset_folder(name,speakers):
	global text
	os.mkdir(os.path.join("data",name))

	with open(os.path.join("data",name,"text"),"w") as f:
		for s in speakers:
			for u in s.utterances:
				f.write(u + " " + text[u] + "\n")

	with open(os.path.join("data",name,"spk2gender"),"w") as f:
		for s in speakers:
			f.write(s.name + " " + s.gender + "\n")

	with open(os.path.join("data",name,"utt2spk"),"w") as f:
		for s in speakers:
			for u in s.utterances:
				f.write(u + " " + s.name + "\n")
	
	with open(os.path.join("data",name,"wav.scp"),"w") as f:
		for s in speakers:
			for u in s.utterances:
				f.write(u + " " + scp[u] + "\n")

create_subset_folder("test",test_spk)
create_subset_folder("mono",mono_spk)
create_subset_folder("tri1",tri1_spk)
create_subset_folder("tri2",tri2_spk)
create_subset_folder("tri3",tri3_spk)