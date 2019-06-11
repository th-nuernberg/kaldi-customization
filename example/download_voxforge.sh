: '
This script does a lot of things:
    1) It downloads the audio data from voxforge and deletes all files which are not needed
    2) It converts all *.flac files into *.wav files using the ffmpeg-converter
    3) It creates the directory structure which we use for training our German identifier with the voxforge audio
    4) It creates all needed files which are necessary in order to run our run.sh script
    5) It copies all the audio data to its destined places and removes all files which are not needed any longer
'

target=$1

calldir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
if [ $# -eq 0 ]
then
	echo "Usage: download_voxforge.sh <target_dir>"
	exit
fi

# Installing ffmpeg which is used for converting the flac-files to wav-files
echo "We want to install ffmpeg to decode flac files, we need your sudo rights for this:"
sudo apt-get install ffmpeg python3 -y

mkdir $target

cd $target
target=$PWD
# Download data
wget http://www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/ -np -r
# copy all tgz files to current directory
cp www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/*.tgz  ./
# clean up
rm -rf www.repository.voxforge1.org

# Unpacking all the compressed audio files into the extracted directory 
for compressed_file in *.tgz; do
    tar -xvzf $compressed_file -C ./
done

# clean up
rm *.tgz

rm Manu-20140323-m8/wav/deM8-44.wav
rm Thomas-20120913-trl/wav/de11-012.wav

# Converting all files from flac to wav
for directory in *; do
    if [ ! -d $directory/wav ]; then
        mkdir $directory/wav
        for flac_file in $directory/flac/*.flac; do
            # Extracting the filename with its extension
            filename_with_extension=$(basename "$flac_file")
            # Removing the extension of the filename
            only_filename=${filename_with_extension%.flac}
            echo $only_filename
            # Converting *.flac to *.wav and store it within the created wav-directory
            ffmpeg -i $flac_file $directory/wav/$only_filename.wav
        done
    fi
done

# Setting up the directory structure for training our first German identifier
# and generating all needed files for the training
mkdir ./data
mkdir ./data/audio
mkdir ./data/etc
mkdir ./data/local
mkdir ./data/local/dict
#TODO!!!!echo "generic_speaker m" >> ../data/etc/spk2gender
echo "sil" >> ./data/local/dict/optional_silence.txt
echo "sil" >> ./data/local/dict/silence_phones.txt
echo "spn" >> ./data/local/dict/silence_phones.txt

# Renaming all audio files within the extracted directory after creating the needed files for training
# Renaming was done in order to ensure a unique name for all audio files
count=0
for directory in *; do
	if [ $directory != data ]
	then
		# For each audio file within these directories
		for audio_file in $directory/wav/*.wav; do
			# Retrieve the filename    
			filename_with_extension=$(basename "$audio_file")
			only_filename=${filename_with_extension%.wav}

			name=$(echo $directory| cut -d '-' -f 1)

			new_name=$name"_"$count"_"$only_filename
			count=$((count+1))

			# Create the text-file which is needed for the training 
			text=$(grep -a $only_filename $directory'/etc/prompts-original' | sed -r "s/$only_filename/$new_name/g")

			echo $text >> ./data/etc/text

			# Create the wav.scp file which is needed for the training 
			echo $new_name $target'/audio/'$new_name'.wav' >> ./data/etc/wav.scp
			# Create the utt2spk file which is needed for the training
			echo "$new_name $name" >> ./data/etc/utt2spk

			# Rename the audio file, in order to ensure unique names
			mv "$directory/wav/$only_filename.wav" "./data/audio/$new_name.wav"
		done
	fi
done


for directory in *; do
	if [ $directory != data ]
	then
		rm -rf $directory
	fi
done

mv data/local ./
mv data/audio ./
mv data/etc ./
rmdir data


cp "$calldir/clean_setup.py" "$target/clean_setup.py"
cp "$calldir/lexicon.txt" "$target/lexicon.txt"

python3 clean_setup.py $target lexicon.txt

phonetisaurus-train -l lexicon.txt -s2d -g -o 8
phonetisaurus-apply --model train/model.fst --word_list voc.tmp -n 2 -l lexicon.txt --beam 10000 -g -t 10000 >> local/dict/lexicon.txt

rm -rf train
rm "voc.tmp"
rm clean_setup.py
rm lexicon.txt
