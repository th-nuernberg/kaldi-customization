FROM python:2.7-alpine3.10
VOLUME ["/g2p_worker/in", "/g2p_worker/out"]
WORKDIR /g2p-worker


RUN apk update && \
    apk upgrade && \
    apk add autoconf-archive automake gfortran git g++ libtool make perl python3-dev py-setuptools tar wget python2-dev python3 python2


# Download and Install OpenFST
RUN wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.2.tar.gz && \
    tar -xvzf openfst-1.6.2.tar.gz && \
    cd openfst-1.6.2/ && \
    ./configure --enable-static --enable-shared --enable-far --enable-ngram-fsts && \
    make -j 4 && \
    make install && \
    cd


# Set environment variable for OpenFST
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib:/usr/local/lib/fst


# Download and build G2P
RUN git clone https://github.com/AdolfVonKleist/Phonetisaurus.git && \
    cd Phonetisaurus && \
    ./configure && \
    make && \
    make install && \
    cd


RUN git clone https://github.com/mitlm/mitlm.git && \
    cd mitlm/ && \
    ./autogen.sh && \
    make && \
    make install && \
    cd


RUN mkdir example && \
    cd example && \
    wget https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict && \
    cat cmudict.dict | perl -pe 's/\([0-9]+\)//; s/\s+/ /g; s/^\s+//; s/\s+$//; @_ = split (/\s+/); $w = shift (@_); $_ = $w."\t".join (" ", @_)."\n";' > cmudict.formatted.dict


RUN phonetisaurus-train --lexicon example/cmudict.formatted.dict --seq2_del 
ADD requirements.txt /g2p-worker/requirements.txt
RUN phonetisaurus-apply --model train/model.fst --word_list requirements.txt

# CMD ["/bin/sh", "/tools/wait-for.sh", "redis:6379", "--", "python", "-u", "/text_prep_worker/text_preparation.py"]
