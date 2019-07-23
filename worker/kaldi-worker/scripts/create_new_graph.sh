#!/bin/bash
. ./path.sh || exit 1

[[ $# -ge 6 ]] && { echo "Usage: create_new_graph.sh <lexicon file> <corpus file> <acoustic model folder> <new graph dir> <temporary dir>"; exit 1; }

lex_file=$1
corp_file=$2
acoustic_model=$3
lm_order=3
new_graph_dir=$4
tmp_dir=$5

new_lang_dir=$tmp_dir/lang
new_local_dir=$tmp_dir/local

mkdir $new_local_dir
mkdir $new_local_dir/dict

echo "Copying lexicon file,appending <SPN> spn as oov"
cp $lex_file $new_local_dir/dict/lexicon.txt
#echo "<SPN> spn" >> $new_local_dir/dict/lexicon.txt
echo "<SIL> sil" >> $new_local_dir/dict/lexicon.txt

echo "Creating phone files from lex. Silence = sil"
python3 extract_phones.py $lex_file "$new_local_dir/dict/nonsilence_phones.txt"
echo "sil" >> $new_local_dir/dict/silence_phones.txt
#echo "spn" >> $new_local_dir/dict/silence_phones.txt
echo "sil" >> $new_local_dir/dict/optional_silence.txt

echo "Preparing Language data"
#utils/prepare_lang.sh $new_local_dir/dict "<SPN>" $new_local_dir/lang $new_lang_dir
utils/prepare_lang.sh $new_local_dir/dict "<SIL>" $new_local_dir/lang $new_lang_dir

echo "Creating Language Model"
echo "making lm.arpa"
loc=`which ngram-count`;
if [ -z $loc ]; then
	    if uname -a | grep 64 >/dev/null; then
	            sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
	    else
	                    sdir=$KALDI_ROOT/tools/srilm/bin/i686
	    fi
	    if [ -f $sdir/ngram-count ]; then
	                    echo "Using SRILM language modelling tool from $sdir"
	                    export PATH=$PATH:$sdir
	    else
	                    echo "SRILM toolkit is probably not installed.
	                            Instructions: tools/install_srilm.sh"
	                    exit 1
	    fi
fi
mkdir $new_lang_dir/tmp
ngram-count -order $lm_order -write-vocab $new_lang_dir/tmp/vocab-full.txt -wbdiscount -text $corp_file -lm $new_lang_dir/tmp/lm.arpa

echo "making G.fst"
arpa2fst --disambig-symbol=#0 --read-symbol-table=$new_lang_dir/words.txt $new_lang_dir/tmp/lm.arpa $new_lang_dir/G.fst

./utils/mkgraph.sh $new_lang_dir $acoustic_model $new_graph_dir

