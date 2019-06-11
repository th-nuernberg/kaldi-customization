#!/bin/bash
. ./path.sh || exit 1
. ./cmd.sh || exit 1
nj=2       # number of parallel jobs - 1 is perfect for such a small dataset
lm_order=1 # language model order (n-gram quantity) - 1 is enough for digits grammar
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }

# Removing previously created data (from last run.sh execution)
rm -rf exp mfcc data/local/dict/lexiconp.txt data/local/lang data/lang data/local/tmp
rm -rf data/test/spk2utt data/test/cmvn.scp data/test/feats.scp data/test/split1  
rm -rf data/mono/spk2utt data/mono/cmvn.scp data/mono/feats.scp data/mono/split1
rm -rf data/tri1/spk2utt data/tri1/cmvn.scp data/tri1/feats.scp data/tri1/split1
rm -rf data/tri2/spk2utt data/tri2/cmvn.scp data/tri2/feats.scp data/tri2/split1
rm -rf data/tri3/spk2utt data/tri3/cmvn.scp data/tri3/feats.scp data/tri3/split1

echo
echo "===== PREPARING ACOUSTIC DATA ====="
echo
# Needs to be prepared by hand (or using self written scripts):
#
# spk2gender  [<speaker-id> <gender>]
# wav.scp     [<uterranceID> <full_path_to_audio_file>]
# text        [<uterranceID> <text_transcription>]
# utt2spk     [<uterranceID> <speakerID>]
# corpus.txt  [<text_transcription>]

# Making spk2utt files
utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt
utils/utt2spk_to_spk2utt.pl data/mono/utt2spk > data/mono/spk2utt
utils/utt2spk_to_spk2utt.pl data/tri1/utt2spk > data/tri1/spk2utt
utils/utt2spk_to_spk2utt.pl data/tri2/utt2spk > data/tri2/spk2utt
utils/utt2spk_to_spk2utt.pl data/tri3/utt2spk > data/tri3/spk2utt

echo
echo "===== FEATURES EXTRACTION ====="
echo
# Making feats.scp files
mfccdir=mfcc
# Uncomment and modify arguments in scripts below if you have any problems with data sorting
# utils/validate_data_dir.sh data/train     # script for checking prepared data - here: for data/train directory

# tool for data proper sorting if needed
utils/fix_data_dir.sh data/test
utils/fix_data_dir.sh data/mono
utils/fix_data_dir.sh data/tri1
utils/fix_data_dir.sh data/tri2
utils/fix_data_dir.sh data/tri3 

steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/test exp/make_mfcc $mfccdir
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/mono exp/make_mfcc $mfccdir
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/tri1 exp/make_mfcc $mfccdir
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/tri2 exp/make_mfcc $mfccdir
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/tri3 exp/make_mfcc $mfccdir

# Making cmvn.scp files
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir
steps/compute_cmvn_stats.sh data/mono exp/make_mfcc/mono $mfccdir
steps/compute_cmvn_stats.sh data/tri1 exp/make_mfcc/tri1 $mfccdir
steps/compute_cmvn_stats.sh data/tri2 exp/make_mfcc/tri2 $mfccdir
steps/compute_cmvn_stats.sh data/tri3 exp/make_mfcc/tri3 $mfccdir

#same data for tri4,tri5
cp -r data/tri3 data/tri4
cp -r data/tri3 data/tri5
cp -r exp/make_mfcc/tri3 exp/make_mfcc/tri4
cp -r exp/make_mfcc/tri3 exp/make_mfcc/tri5

echo
echo "===== PREPARING LANGUAGE DATA ====="
echo
# Needs to be prepared by hand (or using self written scripts):
#
# lexicon.txt           [<word> <phone 1> <phone 2> ...]
# nonsilence_phones.txt [<phone>]
# silence_phones.txt    [<phone>]
# optional_silence.txt  [<phone>]
# Preparing language data
utils/prepare_lang.sh data/local/dict "<%>" data/local/lang data/lang
echo
echo "===== LANGUAGE MODEL CREATION ====="
echo "===== MAKING lm.arpa ====="
echo
loc=`which ngram-count`;
if [ -z $loc ]; then
        if uname -a | grep 64 >/dev/null; then
                sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
        else
                        sdir=$KALDI_ROOT/tools/srilm/bin/i686
        fi
        if [ -f $sdir/ngram-count ]; then
                        echo "Using SRILM language modelling tool from $sdir"
                        export PATH=$PATH:$sdir
        else
                        echo "SRILM toolkit is probably not installed.
                                Instructions: tools/install_srilm.sh"
                        exit 1
        fi
fi
local=data/local
mkdir $local/tmp
ngram-count -order $lm_order -write-vocab $local/tmp/vocab-full.txt -wbdiscount -text data/local/corpus.txt -lm $local/tmp/lm.arpa
echo
echo "===== MAKING G.fst ====="
echo
lang=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst

echo
echo "===== MONO TRAINING ====="
echo
steps/train_mono.sh --nj $nj --cmd "$train_cmd" data/mono data/lang exp/mono || exit 1
echo
echo "===== MONO DECODING ====="
echo
utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/mono/graph data/test exp/mono/decode
echo
echo "===== MONO ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/mono data/lang exp/mono exp/mono_ali || exit 1

echo
echo "===== TRI1 (first triphone pass) TRAINING ====="
echo
steps/train_deltas.sh --cmd "$train_cmd" 2500 10000 data/tri1 data/lang exp/mono_ali exp/tri1 || exit 1
echo
echo "===== TRI1 (first triphone pass) DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode
echo
echo "===== TRI1 ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/tri1 data/lang exp/tri1 exp/tri1_ali || exit 1

echo
echo "===== TRI2 TRAINING ====="
echo
steps/train_deltas.sh --cmd "$train_cmd" 3000 20000 data/tri2 data/lang exp/tri1_ali exp/tri2 || exit 1
echo
echo "===== TRI2 DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri2 exp/tri2/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri2/graph data/test exp/tri2/decode
echo
echo "===== TRI2 ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/tri2 data/lang exp/tri2 exp/tri2_ali || exit 1

echo
echo "===== TRI3 (LDA MLLT) TRAINING ====="
echo
steps/train_lda_mllt.sh --cmd "$train_cmd" 3500 40000 data/tri3 data/lang exp/tri2_ali exp/tri3 || exit 1
echo
echo "===== TRI3 (LDA MLLT) DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri3 exp/tri3/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri3/graph data/test exp/tri3/decode
echo
echo "===== TRI3 (LDA MLLT) ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/tri3 data/lang exp/tri3 exp/tri3_ali || exit 1

echo
echo "===== TRI4 (SAT) TRAINING ====="
echo
steps/train_sat.sh --cmd "$train_cmd" 4500 60000 data/tri4 data/lang exp/tri3_ali exp/tri4 || exit 1
echo
echo "===== TRI4 (SAT) DECODING ====="
echo
utils/mkgraph.sh data/lang exp/tri4 exp/tri4/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri4/graph data/test exp/tri4/decode
echo
echo "===== TRI4 (SAT) ALIGNMENT ====="
echo
steps/align_si.sh --nj $nj --cmd "$train_cmd" data/tri4 data/lang exp/tri4 exp/tri4_ali || exit 1

echo
echo "===== run.sh script is finished ====="
echo
