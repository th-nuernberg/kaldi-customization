#!/bin/bash

##########################################################################################
# This bash prepares the sound recordings for Kaldi.
#   - creates a folder structure inside of $KaldiInstallation/egs/
#   - renames recording files
#   - moves recording files into new structure for training and testing
#   -
##########################################################################################

prepareDirectories()
{
    kaldiHome=$1
    audioHome=$2
    projectName=$3

    prepareKaldiEgsProjectFolder $kaldiHome $projectName
    prepareSoundProjectFolder $audioHome $projectName
}

prepareKaldiEgsProjectFolder()
{
    kaldiHome=$1
    projectName=$2

    # creates and prepares project folder structure in kaldi home egs directory
    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectSoundHome="$kaldiProjectHome/${projectName}_audio"
    projectDataHome="$kaldiProjectHome/data"
    projectDataTrainHome="$projectDataHome/train"
    projectDataTestHome="$projectDataHome/test"
    projectDataLocalHome="$projectDataHome/local"
    projectDataLocalDictHome="$projectDataLocalHome/dict"
    projectConfHome="$kaldiProjectHome/conf"
    projectLocalHome="$kaldiProjectHome/local"

    rm -rf $kaldiProjectHome

    echo "Preparing project folder inside of Kaldi egs installation."
    if [ ! -d $kaldiProjectHome ]
    then
        mkdir $kaldiProjectHome
    fi
        if [ ! -d $projectSoundHome ]
        then
            mkdir $projectSoundHome
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

prepareSoundProjectFolder()
{
    audioHome=$1
    projectName=$2
    
    audioSpeakerHome="$audioHome/speaker"
    audioSpeakerOneHome="$audioSpeakerHome/jackson"
    audioSpeakerTwoHome="$audioSpeakerHome/theo"
    audioSpeakerThreeHome="$audioSpeakerHome/nicolas"
    audioSpeakerFourHome="$audioSpeakerHome/yweweler"
    audioSpeakerTestHome="$audioHome/test"
    audioSpeakerTestOneHome="$audioSpeakerTestHome/jackson"
    audioSpeakerTrainHome="$audioHome/train"
    audioSpeakerTrainTwoHome="$audioHome/train/theo"
    audioSpeakerTrainThreeHome="$audioHome/train/nicolas"
    audioSpeakerTrainFourHome="$audioHome/train/yweweler"

    rm -rf $audioSpeakerHome
    echo "Preparing sound folder structure."
    if [ ! -d $audioSpeakerHome ]
    then
        mkdir $audioSpeakerHome
    fi

        if [ ! -d $audioSpeakerOneHome ]
        then
            mkdir $audioSpeakerOneHome
        fi

        if [ ! -d $audioSpeakerTwoHome ]
        then
            mkdir $audioSpeakerTwoHome
        fi

        if [ ! -d $audioSpeakerThreeHome ]
        then
            mkdir $audioSpeakerThreeHome
        fi

        if [ ! -d $audioSpeakerFourHome ]
        then
            mkdir $audioSpeakerFourHome
        fi

    if [ ! -d $audioSpeakerTestHome ]
    then
        mkdir $audioSpeakerTestHome
    fi

        if [ ! -d $audioSpeakerTestOneHome ]
        then
            mkdir $audioSpeakerTestOneHome
        fi

    if [ ! -d $audioSpeakerTrainHome ]
    then
        mkdir $audioSpeakerTrainHome
    fi

        if [ ! -d $audioSpeakerTrainTwoHome ]
        then
            mkdir $audioSpeakerTrainTwoHome
        fi

        if [ ! -d $audioSpeakerTrainThreeHome ]
        then
            mkdir $audioSpeakerTrainThreeHome
        fi

        if [ ! -d $audioSpeakerTrainFourHome ]
        then
            mkdir $audioSpeakerTrainFourHome
        fi

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

    # copies prepared bash scripts
    bashHome="/home/flo/kaldi/prepare_it_project/templates/bash/"
    cmdShellPath="$bashHome/cmd.sh"
    pathShellPath="$bashHome/path.sh"
    runShellPath="$bashHome/run.sh"
    cp -v  $cmdShellPath $projectHome
    cp -v  $pathShellPath $projectHome
    cp -v  $runShellPath $projectHome

    #copies prepared config files
    configHome="/home/flo/kaldi/prepare_it_project/templates/config/"
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
    textHome="/home/flo/kaldi/prepare_it_project/templates/text"
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
    speakerNameOne="jackson"
    speakerNameTwo="theo"
    speakerNameThree="nicolas"
    speakerNameFour="yweweler"

    audioHome=$1
    cd $audioHome

    speakerHome="$audioHome/speaker"
    speakerHomeOne="$speakerHome/$speakerNameOne"
    speakerHomeTwo="$speakerHome/$speakerNameTwo"
    speakerHomeThree="$speakerHome/$speakerNameThree"
    speakerHomeFour="$speakerHome/$speakerNameFour"

    speakerOneCount=0
    speakerTwoCount=0
    speakerThreeCount=0
    speakerFourCount=0 

    echo $PWD
    cd "../recordings"

    for i in *.wav
    do
        if [[ "$i" =~ $speakerNameOne ]]
        then
            speakerOneCount=$[$speakerOneCount+1]
            cp -v $i $speakerHomeOne
        elif [[ "$i" =~ $speakerNameTwo ]]
        then
            speakerTwoCount=$[$speakerTwoCount+1]
            cp -v $i $speakerHomeTwo
        elif [[ "$i" =~ $speakerNameThree ]]
        then
            speakerThreeCount=$[$speakerThreeCount+1]
            cp -v $i $speakerHomeThree
        elif [[ "$i" =~ $speakerNameFour ]]
        then
            speakerFourCount=$[$speakerFourCount+1]
            cp -v $i $speakerHomeFour
        fi
    done

    echo "Number of recordings from speaker one: $speakerOneCount"
    echo "Number of recordings from speaker two: $speakerTwoCount"
    echo "Number of recordings from speaker three: $speakerThreeCount"
    echo "Number of recordings from speaker four: $speakerFourCount"

    cd "$audioHome"
}

structureRecordings()
{
    audioHome=$1
    speaker="speaker"
    test="test"
    train="train"
    
    # Sortiert die im Directory vorkommenden Files nach ihrer Nummerierung
    iterateOverAllFiles "$speaker/jackson" "$test/jackson" $audioHome
    iterateOverAllFiles "$speaker/yweweler" "$train/yweweler" $audioHome
    iterateOverAllFiles "$speaker/nicolas" "$train/nicolas" $audioHome
    iterateOverAllFiles "$speaker/theo" "$train/theo" $audioHome

    echo "Renaming files..."
    renameRecordingFiles "$audioHome/test/jackson"
    renameRecordingFiles "$audioHome/train/nicolas"
    renameRecordingFiles "$audioHome/train/theo"
    renameRecordingFiles "$audioHome/train/yweweler"
    echo "Finished renaming.."
}

iterateOverAllFiles()
{
    speakerDir=$1
    destinationDir=$2
    audioHome=$3

    cd $speakerDir 
    for file in *.wav
    do
        cp -v $file "$audioHome/$destinationDir"        
    done

    cd $audioHome
}

renameRecordingFiles()
{
    # Aktueller Name: {number}_{speaker}_{0-49}.wav
    # Bevorzugter Name: {speaker}_{number}_{0-*}.wav
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

cleanupRecordings()
{
    soundHome=$1
    speakerHome="$soundHome/speaker"
    recordingHome="$soundHome/recordings"
    echo "Cleaning up not needed recording files..."
    rm -rf $soundHome
    # rm -rf recordings
    echo "Finished clean up..."
}

moveRecordingsToKaldi()
{
    kaldiHome=$1
    projectName=$2
    soundHome=$3
    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectSoundHome="$kaldiProjectHome/${projectName}_audio"
    test="test"
    train="train"

    cd $soundHome
    mv -v $test $projectSoundHome
    mv -v $train $projectSoundHome
}

copyConfiguredTools()
{
    
    kaldiHome=$1
    projectName=$2
    kaldiProjectHome="$kaldiHome/egs/$projectName"
    projectLocalHome="$kaldiProjectHome/local/"

    bashHome="/home/flo/kaldi/prepare_it_project/templates/bash"
    folderHome="/home/flo/kaldi/prepare_it_project/templates/folders"

    cp -r "$folderHome/utils" $kaldiProjectHome
    cp -r "$folderHome/steps" $kaldiProjectHome
    cp "$bashHome/score.sh" $projectLocalHome
}

# set home folder of kaldi and sound recordings => TODO must be set once on the server!
userName=$(eval echo ~$USER)
helperWorkspace="$userName/kaldi/checkout/kaldi-customization/helper"

#kaldiHome="$userName/kaldi/kaldi"
kaldiHome="$helperWorkspace/dummy"
soundHome="$userName/kaldi/checkout/kaldi-customization/worker/kaldi-worker/digits/data_audio/dummy"
projectName="digits"

# for testing only -> needs to be adapted!!!!
mkdir -p "$kaldiHome/egs/$projectName"
mkdir -p "$soundHome"


# prepare tasks
prepareDirectories $kaldiHome $soundHome $projectName
prepareRecordings $soundHome
structureRecordings $soundHome
moveRecordingsToKaldi $kaldiHome $projectName $soundHome
cleanupRecordings $soundHome
copyConfiguredTools $kaldiHome $projectName