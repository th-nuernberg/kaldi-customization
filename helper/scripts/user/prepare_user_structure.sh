#!/bin/bash

#################################################################################################
# prepare_user_strcture.sh  creates the expected folder and file structure for the execution
# of Kaldi as a user (without the training session) while using the existing kaldi
# trained model
#################################################################################################
# Methods of the shell script:
# prepareDirectories(); creates the folder structure inside the Kaldi egs folder
# createProjectFiles(): creates and copies project files for data, config and shell scripts
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
    projectDataHome="$kaldiProjectHome/data"
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

        if [ ! -d $projectDataHome ]
        then
            mkdir $projectDataHome
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

    ceateProjectFiles $kaldiProjectHome $projectConfHome $projectDataLocalHome $projectDataLocalDictHome

    echo "Finished..."
}

ceateProjectFiles()
{
    projectHome=$1
    projectConfHome=$2
    projectDataLocalHome=$3
    projectDataLocalDictHome=$4

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
    speakerCount=0
    kaldiHome=$1
    projectName=$2
    audioHome=$3

    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectSoundHome="$kaldiProjectHome/${projectName}_audio"
    test="test"

    cd "$audioHome/recordings"
    
    # copies and renames the recordings files to the kaldi/egs/project/audio folders
    echo "Starting to prepare recording files..."
    for i in *.wav
    do
        speakerCount=$[$speakerCount+1]
        # copies and renames recording files
        cp -v $i "$projectSoundHome/$test/speaker_${speakerCount}.wav"
    done

    echo "Number of recordings: $speakerCount !"
    echo "Finished to prepare recording files!"
    cd "$audioHome"
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
projectName="digits_user"

# prepare tasks
prepareDirectories $kaldi $projectName

# copies recording files into egs project directory
prepareRecordings $kaldi $projectName $soundHome 

# copy template files into project folder
copyConfiguredTools $kaldiHome $projectName