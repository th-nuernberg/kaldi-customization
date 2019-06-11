import sys
import codecs
import re

if(len(sys.argv) != 3):
	print("Usage: python3 clean_setup.py <target_dir> <lexicon_file>")
	exit()

target_dir = sys.argv[1]
lexicon_file = sys.argv[2]

def clean_corpus_string(string):
	return string.lower().replace('ü','"u').replace('ö','"o').replace('ä','"a').replace('ß','"s').replace('§','" paragraph ').replace(',',' , ').replace('.',' . ').replace('!',' ! ').replace('?',' ? ').replace('%',' prozent ').replace('+','').replace('1',' eins ').replace('2',' zwei ').replace('3',' drei ').replace('4',' vier ').replace('5',' f"unf ').replace('6',' sechs ').replace('7',' sieben ').replace('8',' acht ').replace('9',' neun ').replace('0',' null ').replace(':',' . ').replace('{',' ').replace('}',' ').replace(';',' , ').replace('(',' ').replace(')',' ').replace('=',' ').replace('?',' . ').replace('-',' . ').replace('&',' und ').replace(',','.').replace('.','<%>')

phones = set()
with open(lexicon_file,"r") as lex:
	for line in lex:
		pron = "".join(line.split()[1:])
		x=""
		for c in pron: x = c + x
		p=set()
		b=False
		for c in x:
			if c is ":":
				b=True
			else:
				if b:
					p = p.union(set([c+":"]))
					b = False
				else:
					p = p.union(set([c]))
		phones = phones.union(p)

print("Found ",len(phones), " phones:\n",phones)

with open(target_dir+"/local/dict/nonsilence_phones.txt","w") as phonestxt:
	for s in phones:
		phonestxt.write(s+"\n")

print("Cleaning text file...")
print("\t Encoding...")
buffer= []
with open(target_dir+"/etc/text", "rb") as f:
	byte = f.read(1)
	while byte != b"":
		# Do stuff with byte.
		byte = f.read(1)
		if int.from_bytes(byte,"little") == 0xFC: #ü
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('bc'))
		elif int.from_bytes(byte,"little") == 0xF6: #ö
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('b6'))
		elif int.from_bytes(byte,"little") == 0xE4: #ä
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('a4'))
		elif int.from_bytes(byte,"little") == 0xDF: #ß
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('9f'))
		elif int.from_bytes(byte,"little") == 0xC4: #Ä
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('84'))
		elif int.from_bytes(byte,"little") == 0xDC: #Ü
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('9c'))
		elif int.from_bytes(byte,"little") == 0xD6: #Ö
			buffer.append(bytes.fromhex('c3'))
			buffer.append(bytes.fromhex('96'))
		elif int.from_bytes(byte,"little") in (0xC2,0xB0,0xAD,0xB4): #remove unnecessary bytes
			buffer.append(b'')
		elif int.from_bytes(byte,"little") == 0xA7: #§
			#buffer.append(bytes.fromhex('c2'))
			buffer.append(b'Paragraph')
		elif int.from_bytes(byte,"little") != 0x00: #if not empty
			buffer.append(byte)

with open(target_dir+"/etc/text", "wb") as f:
	for b in buffer:
		f.write(b)

print("\t Fix openpento...")

buffer = []
with open(target_dir+"/etc/text", "r") as f:
	for line in f:
		buffer.append(re.sub(r' open.*','',line))

with open(target_dir+"/etc/text", "w") as f:
	for line in buffer:
		f.write(line)

print("\t Fix special characters and lower all...")

buffer = []
corpus = []
with open(target_dir+"/etc/text", "r") as f:
	for line in f:
		fi = line.split()[0]
		utt = " ".join(clean_corpus_string(" ".join(line.split()[1:])).split())
		buffer.append((fi,utt))
		corpus.append(utt)

with open(target_dir+"/etc/text", "w") as f:
	for line in buffer:
		f.write(line[0]+" "+line[1]+"\n")

#write corpus
with open(target_dir+"/local/corpus.txt", "w") as f:
	for line in corpus:
		f.write(line+"\n")

print("Creating new vocabulary")
voc = set()
with open(target_dir+"/etc/text", "r") as f:
	for line in f:
		words = set(line.split()[1:])
		voc = voc.union(words)

with open("voc.tmp","w") as f:
	for v in voc:
		f.write(v+"\n")
print("Found ",len(voc), " words in vocab")

lex = list()
with open(target_dir + "/local/dict/lexicon.txt") as f:
    for line in f:
        x = line.split()
        prn = "".join(x[1:])

        phones = list()
        buf=""
        for c in reversed(prn):
            if c is ":":
                buf = c
            else:
                phones.append(c + buf)
                buf = ""
        
        phones = reversed(phones)

        lex.append((x[0],phones))

with open(target_dir + "/local/dict/lexicon.txt","w") as f:
    for l in lex:
        f.write(l[0] + " " + " ".join(l[1])+ "\n")