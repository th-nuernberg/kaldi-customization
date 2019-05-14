#!/bin/bash

##########################################################################################################
# prepare_developer_data_files.sh fills the expected folders with text, path etc. of the recording files
##########################################################################################################
# Methods of the shell script:
# fillData(): fills the wav.scp and utt2spk with the speaker id and the path to the recording file
# for test and train data
# fillSpk2Gender(): sets the speaker and gender to test and train data
##########################################################################################################

fillData()
{
    pathForFilling=$1
    pathForSaving=$2
    prefix=$3

    pathToWavScp="$pathForSaving/wav.scp"
    pathToUtt2Spk="$pathForSaving/utt2spk"

    cd $pathForFilling

    # gets all recording files with the same prefix
    fileList="$(ls $prefix'_'* | sort -n -t _ -k 3)"
    echo "Starting to fill test data files..."
    for file in $fileList
    do
        IFS='_' read -ra ADDR <<< "$file"
        # writes speakerID and path to recording file to wav.scp
        echo "${file%%.wav}  ${ADDR[0]}" >> $pathToWavScp
        # writes recording file name and speakerID to utt2spk         
        echo "${file%%.wav}  ${pathForFilling}/$file" >> $pathToUtt2Spk  
    done
    echo "Finished fillng test data files!"
}

fillSpk2Gender()
{
    pathToSpk2Gender=$1
    echo "Setting spk2Gender..."
    # writes the speakerID and the gender into the file
    echo "speaker m" >> $pathToSpk2Gender
    echo "Finished setup of spk2gender!"
}

# TODO needs to be adjusted!!!!
projectName="digits_developer"

kaldi=$(echo $KALDI)
kaldiProjectHome="$kaldi/egs/$projectName"
kaldiProjectAudioHome="$kaldiProjectHome/${projectName}_audio"
kaldiProjectDataHome="$kaldiProjectHome/data"

# fills utt2spk and wav.scp files!
fillData "$kaldiProjectAudioHome/test/" "$kaldiProjectDataHome/test/" "speaker"
fillData "$kaldiProjectAudioHome/train/" "$kaldiProjectDataHome/train/" "speaker"

# sets spk2gender with a single speaker (male)
fillSpk2Gender "$kaldiProjectDataHome/test/spk2gender"
fillSpk2Gender "$kaldiProjectDataHome/train/spk2gender"