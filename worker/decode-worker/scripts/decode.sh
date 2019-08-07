#!/bin/bash

set -e -o pipefail
[[ $# -ge 4 ]] && { echo "Usage: create_new_graph.sh <workspace> <acoustic model> <graph>"; exit 1; }

nj=1
workspace=$1
acoustic_model=$2
graph=$3

. ./cmd.sh
. ./path.sh

utils/utt2spk_to_spk2utt.pl $workspace/data/utt2spk > $workspace/data/spk2utt
utils/fix_data_dir.sh $workspace/data
#steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" $workspace $workspace/make_mfcc $workspace/mfcc
#steps/compute_cmvn_stats.sh $workspace $workspace/make_mfcc $workspace/mfcc


echo "$0: creating high-resolution MFCC features"

utils/copy_data_dir.sh $workspace/data $workspace/data_hires
steps/make_mfcc.sh --nj $nj --mfcc-config conf/mfcc_hires.conf --cmd "$train_cmd" $workspace/data_hires
steps/compute_cmvn_stats.sh $workspace/data_hires
utils/fix_data_dir.sh $workspace/data_hires

# Extract iVectors for the decode data, but in this case we don't need the speed pertubation (sp).
steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj $nj \
	$workspace/data_hires $acoustic_model/extractor $workspace/ivectors_data_hires


frames_per_chunk=40
chunk_left_context=40
chunk_right_context=0

steps/nnet3/decode.sh --extra-left-context $chunk_left_context \
	--extra-right-context $chunk_right_context \
	--extra-left-context-initial 0 \
	--extra-right-context-final 0 \
	--frames-per-chunk $frames_per_chunk \
	--nj $nj --cmd "$decode_cmd"  --num-threads 4 \
	--online-ivector-dir $workspace/ivectors_data_hires \
	$graph $workspace/data_hires $acoustic_model/decode || exit 1
