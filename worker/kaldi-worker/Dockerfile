FROM kaldi-base
MAINTAINER Tobias Kruse <***REMOVED***>


ADD digits /kaldi/egs/digits

RUN cp -R /kaldi/egs/wsj/s5/utils /kaldi/egs/digits/utils && \
    cp -R /kaldi/egs/wsj/s5/steps /kaldi/egs/digits/steps && \
    mkdir /kaldi/egs/digits/local && cp /kaldi/egs/voxforge/s5/local/score.sh /kaldi/egs/digits/local/score.sh && \
    cd /kaldi/egs/digits/ && \
        perl -pi -e 's/kaldi\.XXXX\)/kaldi.XXXXXX)/' ./utils/*_data_dir.sh && \
        ./utils/fix_data_dir.sh ./data/train && \
        ./utils/fix_data_dir.sh ./data/test


ENTRYPOINT ["/bin/ash"]
