#!/bin/bash

fillTestData()
{
    pathForFilling=$1
    pathForSaving=$2
    prefix=$3

    pathToWavScp="$pathForSaving/wav.scp"
    pathToUtt2Spk="$pathForSaving/utt2spk"

    cd $pathForFilling

    fileList="$(ls $prefix'_'* | sort -n -t _ -k 3)"
    echo "Starting to fill test data files..."
    for file in $fileList
    do
        IFS='_' read -ra ADDR <<< "$file"
        echo "${file%%.wav}  ${ADDR[0]}" >> $pathToWavScp                
        echo "${file%%.wav}  ${pathForFilling}/$file" >> $pathToUtt2Spk  
    done
    echo "Finished fillng test data files!"
}

fillSpk2Gender()
{
    pathToSpk2Gender=$1
    echo "Setting spk2Gender..."
    echo "speaker m" >> $pathToSpk2Gender
    echo "Finished setup of spk2gender!"
}

projectName="digits_developer"

kaldi=$(echo $KALDI)
kaldiProjectHome="$kaldi/egs/$projectName"
kaldiProjectAudioHome="$kaldiProjectHome/${projectName}_audio"
kaldiProjectDataHome="$kaldiProjectHome/data"

# fills utt2spk and wav.scp files!
fillTestData "$kaldiProjectAudioHome/test/" "$kaldiProjectDataHome/test/" "speaker"
fillTestData "$kaldiProjectAudioHome/train/" "$kaldiProjectDataHome/train/" "speaker"

# sets spk2gender with a single speaker (male)
fillSpk2Gender "$kaldiProjectDataHome/test/spk2gender"
fillSpk2Gender "$kaldiProjectDataHome/train/spk2gender"