import sys

if(len(sys.argv) != 3):
	print("Usage: extract_phones.py <lexicon file> <out file>")
	exit(1)
lex_file = sys.argv[1]
out_file = sys.argv[2]

phones = set()
with open(lex_file) as f:
	for line in f:
		phones = phones.union(set(line.split()[1:]))


phones = [x for x in phones if x != "sil"]

print("Extracted",len(phones),"Phones")

with open(out_file,"w+") as f:
	for phone in phones:
		f.write(phone+"\n")

