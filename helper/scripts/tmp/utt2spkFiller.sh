#!/bin/bash

uttSpkFiller()
{

pathForFilling=$1
pathForSaving=$2
prefix=$3

cd $pathForFilling

fileList="$(ls $prefix'_'* | sort -n -t _ -k 3)"

for file in $fileList
do
    IFS='_' read -ra ADDR <<< "$file"   
    echo "${file%%.wav}  ${ADDR[0]}" >> $pathForSaving          
done
}

uttSpkFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/test/jackson" "/home/dino/kaldi/kaldi/egs/digits/data/test/utt2spk" "jackson"
uttSpkFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/train/nicolas" "/home/dino/kaldi/kaldi/egs/digits/data/train/utt2spk" "nicolas"
uttSpkFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/train/theo" "/home/dino/kaldi/kaldi/egs/digits/data/train/utt2spk" "theo"
uttSpkFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/train/yweweler" "/home/dino/kaldi/kaldi/egs/digits/data/train/utt2spk" "yweweler"