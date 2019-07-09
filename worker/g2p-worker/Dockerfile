FROM python:2.7-alpine3.10
VOLUME ["/g2p_worker/in", "/g2p_worker/out"]
WORKDIR /g2p-worker


ADD src/g2p.py /g2p-worker/ 
ADD wait-for.sh /g2p-worker/ 
ADD src/minio_communication.py /g2p-worker/ 
ADD requirements.txt /g2p-worker/

RUN apk update && \
    apk upgrade && \
    apk add autoconf-archive automake gfortran git g++ libtool libxml2-dev libxslt-dev && \
            make perl python3 python3-dev python2-dev python2 py-setuptools tar wget   && \
    pip install -r requirements.txt

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

CMD ["/bin/sh", "/g2p-worker/wait-for.sh", "redis:6379", "--", "python", "-u", "/g2p-worker/g2p.py"]
