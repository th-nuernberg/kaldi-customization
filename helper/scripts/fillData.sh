#!/bin/bash

wavFiller()
{
    pathForFilling=$1
    pathForSaving=$2
    prefix=$3

    cd $pathForFilling

    fileList="$(ls $prefix'_'* | sort -n -t _ -k 3)"

    for file in $fileList
    do
        IFS='_' read -ra ADDR <<< "$file"   
        echo "${file%%.wav}  ${pathForFilling}/$file" >> $pathForSaving
    done
}

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
        #echo "${file%%.wav}  ${pathForFilling}/$file" >> $pathForSaving          
    done
}

userName=$(eval echo ~$USER)
#kaldiHome="$userName/kaldi/kaldi"
kaldiHome="$userName/kaldi/prepare_it_project/dummy"
soundHome="$userName/kaldi/prepare_it_project/sound/dummy"
projectName="endgame"

kaldiProjectHome="$kaldiHome/egs/$projectName"
kaldiProjectAudioHome="$kaldiProjectHome/${projectName}_audio"
kaldiProjectDataHome="$kaldiProjectHome/data"

wavFiller "$kaldiProjectAudioHome/test/jackson" "$kaldiProjectDataHome/test/wav.scp" "jackson"
wavFiller "$kaldiProjectAudioHome/train/nicolas" "$kaldiProjectDataHome/train/wav.scp" "nicolas"
wavFiller "$kaldiProjectAudioHome/train/theo" "$kaldiProjectDataHome/train/wav.scp" "theo"
wavFiller "$kaldiProjectAudioHome/train/yweweler" "$kaldiProjectDataHome/train/wav.scp" "yweweler"


uttSpkFiller "$kaldiProjectAudioHome/test/jackson" "$kaldiProjectDataHome/test/utt2spk" "jackson"
uttSpkFiller "$kaldiProjectAudioHome/train/nicolas" "$kaldiProjectDataHome/train/utt2spk" "nicolas"
uttSpkFiller "$kaldiProjectAudioHome/train/theo" "$kaldiProjectDataHome/train/utt2spk" "theo"
uttSpkFiller "$kaldiProjectAudioHome/train/yweweler" "$kaldiProjectDataHome/train/utt2spk" "yweweler"