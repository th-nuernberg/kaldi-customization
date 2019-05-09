#!/bin/bash

wavFiller()
{

pathForFilling=$1
pathForSaving=$2
prefix=$3

cd $pathForFilling

#fileList="$(ls $prefix'_'* | sort)"
fileList="$(ls $prefix'_'* | sort -n -t _ -k 3)"

for file in $fileList
do
    IFS='_' read -ra ADDR <<< "$file"   
    echo "${file%%.wav}  ${pathForFilling}/$file" >> $pathForSaving
done
}

wavFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/test/jackson" "/home/dino/kaldi/kaldi/egs/digits/data/test/wav.scp" "jackson"
wavFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/train/nicolas" "/home/dino/kaldi/kaldi/egs/digits/data/train/wav.scp" "nicolas"
wavFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/train/theo" "/home/dino/kaldi/kaldi/egs/digits/data/train/wav.scp" "theo"
wavFiller "/home/dino/kaldi/kaldi/egs/digits/digits_audio/train/yweweler" "/home/dino/kaldi/kaldi/egs/digits/data/train/wav.scp" "yweweler"