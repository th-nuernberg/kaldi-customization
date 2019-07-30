#!/bin/bash

if [ $# != 2 ]; then
   echo "Usage: run.sh <model-dir> <probe-dir>"
   exit 1;
fi

# Defining Kaldi root directory
export KALDI_ROOT=`pwd`/..

# Setting paths to useful tools
export PATH=$PWD/utils/:$KALDI_ROOT/src/bin:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/src/fstbin/:$KALDI_ROOT/src/gmmbin/:$KALDI_ROOT/src/featbin/:$KALDI_ROOT/src/lmbin/:$KALDI_ROOT/src/sgmm2bin/:$KALDI_ROOT/src/fgmmbin/:$KALDI_ROOT/src/latbin/:$KALDI_ROOT/OpenBLAS/install/lib:$KALDI_ROOT/OpenBLAS/install/bin:$PWD:$PATH

# Defining audio data directory (modify it for your installation directory!)
export DATA_ROOT="$1/audio"

# Enable SRILM
. $KALDI_ROOT/tools/env.sh
# Variable needed for proper data sorting
export LC_ALL=C

# Setting local system jobs (local CPU - no external clusters)
export train_cmd=run.pl
export decode_cmd=run.pl

nj=1       # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=1 # language model order (n-gram quantity) - 1 is enough for digits grammar

prep_probe.sh $2

#utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1

utils/utt2spk_to_spk2utt.pl $2/utt2spk > $2/spk2utt
#utils/fix_data_dir.sh $2 || exit 1

mfccdir=mfcc
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" $2 $2/exp/make_mfcc/test $mfccdir || exit 1
steps/compute_cmvn_stats.sh $2 $2/exp/make_mfcc/test $mfccdir || exit 1

steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" --skip-scoring true $1/graph $2 $1/decode || exit 1

cat $1/decode/log/decode.1.log | grep ^generic | sed 's/[^ ]* //' > $1/decode/text
