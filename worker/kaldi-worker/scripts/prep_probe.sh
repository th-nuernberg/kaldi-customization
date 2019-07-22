#!/bin/bash

if [ $# != 1 ]; then
   echo "Usage: prep_probe.sh <probe-dir>"
   exit 1;
fi

mkdir -p $1

echo "generic m" > "$1/spk2gender"
echo "generic generic" > "$1/utt2spk"
echo "generic $1/generic.wav" > "$1/wav.scp"
