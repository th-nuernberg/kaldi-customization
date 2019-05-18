#!/bin/bash

#################################################################################################
# prepare_developer_strcture.sh creates the expected folder and file structure for the execution
# of Kaldi as a developer with the posibility to extend the pretrained kaldi model
#################################################################################################
# Methods of the shell script:
# prepareDirectories(); creates the folder structure inside the Kaldi egs folder
# createProjectFiles(): creates and copies project files for data, config and shell scripts
# prepareRecordings(): copies and renames recording files into the created project structure
# prepareRecordings(): copies and renames recording files into the created project structure
# copyConfiguredTools(): copies pre-configured tools e.g. utils, steps to the project structure
#################################################################################################

prepareDirectories()
{
    kaldiHome=$1
    projectName=$2

    # creates and prepares project folder structure in kaldi home egs directory
    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectSoundHome="$kaldiProjectHome/${projectName}_audio"
    projectSoundTestHome="$projectSoundHome/test"
    projectSoundTrainHome="$projectSoundHome/train"
    projectDataHome="$kaldiProjectHome/data"
    projectDataTrainHome="$projectDataHome/train"
    projectDataTestHome="$projectDataHome/test"
    projectDataLocalHome="$projectDataHome/local"
    projectDataLocalDictHome="$projectDataLocalHome/dict"
    projectConfHome="$kaldiProjectHome/conf"
    projectLocalHome="$kaldiProjectHome/local"

    rm -rf $kaldiProjectHome

    # creates the project structure
    echo "Preparing project folder inside of Kaldi egs installation."
    if [ ! -d $kaldiProjectHome ]
    then
        mkdir $kaldiProjectHome
    fi
        if [ ! -d $projectSoundHome ]
        then
            mkdir $projectSoundHome
        fi
            if [ ! -d $projectSoundTestHome ]
            then
                mkdir $projectSoundTestHome
            fi
            
            if [ ! -d $projectSoundTrainHome ]
            then
                mkdir $projectSoundTrainHome
            fi

        if [ ! -d $projectDataHome ]
        then
            mkdir $projectDataHome
        fi
            if [ ! -d $projectDataTrainHome ]
            then
                mkdir $projectDataTrainHome
            fi

            if [ ! -d $projectDataTestHome ]
            then
                mkdir $projectDataTestHome
            fi

            if [ ! -d $projectDataLocalHome ]
            then
                mkdir $projectDataLocalHome
            fi

                if [ ! -d $projectDataLocalDictHome ]
                then
                    mkdir $projectDataLocalDictHome
                fi
        if [ ! -d $projectConfHome ]
        then
            mkdir $projectConfHome
        fi

        if [ ! -d $projectLocalHome ]
        then
            mkdir $projectLocalHome
        fi

    ceateProjectFiles $kaldiProjectHome $projectConfHome $projectDataTrainHome $projectDataTestHome $projectDataLocalHome $projectDataLocalDictHome

    echo "Finished..."
}

ceateProjectFiles()
{
    projectHome=$1
    projectConfHome=$2
    projectDataTrainHome=$3
    projectDataTestHome=$4
    projectDataLocalHome=$5
    projectDataLocalDictHome=$6

    kaldicustom=$(echo $KALDICUSTOM)
    templates="$kaldicustom/helper/templates"

    # copies prepared bash scripts
    bashHome="$templates/bash/"
    cmdShellPath="$bashHome/cmd.sh"
    pathShellPath="$bashHome/path.sh"
    runShellPath="$bashHome/run.sh"
    cp -v  $cmdShellPath $projectHome
    cp -v  $pathShellPath $projectHome
    cp -v  $runShellPath $projectHome

    #copies prepared config files
    configHome="$templates/config/"
    mfccConfigPath="$configHome/mfcc.conf"
    decodeConfigPath="$configHome/decode.config"
    cp -v  $mfccConfigPath $projectConfHome
    cp -v  $decodeConfigPath $projectConfHome

    # creates train speaker files
    touch "$projectDataTrainHome/spk2gender"
    touch "$projectDataTrainHome/wav.scp"
    touch "$projectDataTrainHome/text"
    touch "$projectDataTrainHome/utt2spk"

    # creates test speaker files
    touch "$projectDataTestHome/spk2gender"
    touch "$projectDataTestHome/wav.scp"
    touch "$projectDataTestHome/text"
    touch "$projectDataTestHome/utt2spk"

    # copies prepared local home files
    textHome="$templates/text"
    corpusTextPath="$textHome/corpus.txt"
    cp -v  $corpusTextPath $projectDataLocalHome

    # copies prepared local dict home files
    lexiconPath="$textHome/lexicon.txt"
    nonsilencePhonesPath="$textHome/nonsilence_phones.txt"
    silencePhonesPath="$textHome/silence_phones.txt"
    optionalSilencePath="$textHome/optional_silence.txt"
    cp -v $lexiconPath $projectDataLocalDictHome
    cp -v $nonsilencePhonesPath $projectDataLocalDictHome
    cp -v $silencePhonesPath $projectDataLocalDictHome
    cp -v $optionalSilencePath $projectDataLocalDictHome
}

prepareRecordings()
{
    kaldiHome=$1
    projectName=$2
    audioHome=$3

    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectSoundHome="$kaldiProjectHome/${projectName}_audio"
    test="test"
    train="train"

    cd "$audioHome/recordings"
    
    # copies and renames the recordings files to the kaldi/egs/project/audio folders
    copySoundFiles $test $projectSoundHome
    copySoundFiles $train $projectSoundHome

    cd "$audioHome"
}

copySoundFiles()
{
    speakerCount=0
    target=$1
    projectSoundHome=$2

    echo "Starting to prepare $target recording files..."
    for i in *.wav
    do
        speakerCount=$[$speakerCount+1]
        # copies and renames recording files
        cp -v $i "$projectSoundHome/$target/speaker_${speakerCount}.wav"
    done

    echo "Number of $target recordings: $speakerCount !"
    echo "Finished to prepare $target recording files!"
}

copyConfiguredTools()
{
    kaldiHome=$1
    projectName=$2
    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectLocalHome="$kaldiProjectHome/local/"

    kaldicustom=$(echo $KALDICUSTOM)
    templates="$kaldicustom/helper/templates"
    bashHome="$templates/bash"
    folderHome="$templates/folders"

    cp -r "$folderHome/utils" $kaldiProjectHome
    cp -r "$folderHome/steps" $kaldiProjectHome
    cp "$bashHome/score.sh" $projectLocalHome
}

# IMPORTANT: set env var for kaldi and kaldi custom repo!
kaldi=$(echo $KALDI)
kaldicustom=$(echo $KALDICUSTOM)
helperWorkspace="$kaldicustom/helper"

# TODO needs to be adjusted!!!!
soundHome="/home/flo/kaldi/checkout/GER/"
projectName="digits_developer"

# prepare tasks
prepareDirectories $kaldi $projectName

# copies recording files into egs project directory
prepareRecordings $kaldi $projectName $soundHome 

# copy template files into project folder
copyConfiguredTools $kaldiHome $projectName