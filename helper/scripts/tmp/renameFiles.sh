#!/bin/bash

# Dieses Script verändert alle Dateinamen, sodass es keinerlei Sortierprobleme mehr mit Kaldi gibt.

# Aktueller Name: {number}_{speaker}_{0-49}.wav
# Bevorzugter Name: {speaker}_{number}_{0-*}.wav

renameFiles(){

dirToRename=$1
cd "$dirToRename"

record=0

for file in *.wav
do
    number=0
    speaker=""
    count=0
    IFS='_' read -ra ADDR <<< "$file"
    for part in "${ADDR[@]}"; do
        if [ $count -eq 0 ]
        then
            number=$part
        elif [ $count -eq 1 ]
        then
            speaker=$part
        fi
        count=$[$count+1]
    done
    record=$[$record+1]
    count=0
    mv "$dirToRename/$file" "$dirToRename/$speaker""_""$number""_""$record"".wav"
    
done
}

echo "Starting to rename the files of jackson"
renameFiles "/home/flo/kaldi/kaldi/egs/digits/digits_audio/test/jackson"
echo "Finished to rename the files of jackson"
echo "-----------------------------------------------------"

echo "Starting to rename the files of nicolas"
renameFiles "/home/flo/kaldi/kaldi/egs/digits/digits_audio/train/nicolas"
echo "Finished to rename the files of nicolas"
echo "-----------------------------------------------------"

echo "Starting to rename the files of theo"
renameFiles "/home/flo/kaldi/kaldi/egs/digits/digits_audio/train/theo"
echo "Finished to rename the files of theo"
echo "-----------------------------------------------------"

echo "Starting to rename the files of yweweler"
renameFiles "/home/flo/kaldi/kaldi/egs/digits/digits_audio/train/yweweler"
echo "Finished to rename the filles of yweweler."
echo "Script finished successfully"
