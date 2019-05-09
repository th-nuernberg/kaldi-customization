#!/bin/bash

# utteranceID whitespace numbers

# "/home/dino/kaldi/kaldi/egs/digits/digits_audio/test/jackson"


textFiller(){

pathForFilling=$1
pathForSaving=$2
prefix=$3

cd $pathForFilling

fileList="$(ls $prefix'_'* | sort -n -t _ -k 3)"

count=0
for file in $fileList
do
    IFS='_' read -ra ADDR <<< "$file"
    if [ "${ADDR[1]}" = "0" ]
    then
        echo "${file%%.wav}  zero" >> $pathForSaving    
    elif [ "${ADDR[1]}" = "1" ]
    then 
        echo "${file%%.wav}  one" >> $pathForSaving    
    elif [ "${ADDR[1]}" = "2" ]
    then 
        echo "${file%%.wav}  two" >> $pathForSaving        
    elif [ "${ADDR[1]}" = "3" ]
    then 
        echo "${file%%.wav}  three" >> $pathForSaving        
    elif [ "${ADDR[1]}" = "4" ]
    then 
        echo "${file%%.wav}  four" >> $pathForSaving        
    elif [ "${ADDR[1]}" = "5" ]
    then 
        echo "${file%%.wav}  five" >> $pathForSaving        
    elif [ "${ADDR[1]}" = "6" ]
    then 
        echo "${file%%.wav}  six" >> $pathForSaving        
    elif [ "${ADDR[1]}" = "7" ]
    then 
        echo "${file%%.wav}  seven" >> $pathForSaving        
    elif [ "${ADDR[1]}" = "8" ]
    then 
            echo "${file%%.wav}  eight" >> $pathForSaving    
    elif [ "${ADDR[1]}" = "9" ]
    then 
        echo "${file%%.wav}  nine" >> $pathForSaving        
    fi        
done

}


textFiller "/home/flo/kaldi/kaldi/egs/digits/digits_audio/test/jackson" "/home/dino/kaldi/kaldi/egs/digits/data/test/text" "jackson"
textFiller "/home/flo/kaldi/kaldi/egs/digits/digits_audio/train/nicolas" "/home/dino/kaldi/kaldi/egs/digits/data/train/text" "nicolas"
textFiller "/home/flo/kaldi/kaldi/egs/digits/digits_audio/train/theo" "/home/dino/kaldi/kaldi/egs/digits/data/train/text" "theo"
textFiller "/home/flo/kaldi/kaldi/egs/digits/digits_audio/train/yweweler" "/home/dino/kaldi/kaldi/egs/digits/data/train/text" "yweweler"
