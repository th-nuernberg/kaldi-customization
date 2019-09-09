FROM python:2.7-alpine3.10
LABEL maintainer="Dino Pehratovic <***REMOVED***>"

RUN mkdir /data_prep_worker/ && \
    mkdir /data_prep_worker/in/ && \
    mkdir /data_prep_worker/out/ && \
    mkdir /tools/

ADD worker/data-preparation-worker/requirements.txt /data_prep_worker/requirements.txt
WORKDIR /data_prep_worker

RUN apk update && \
    apk upgrade && \
    apk add autoconf-archive automake gfortran git g++ libtool libxml2-dev libxslt-dev \
            make perl python3 python3-dev python2-dev python2 py-setuptools tar wget   && \
    pip install -r requirements.txt

# Download and Install OpenFST
RUN wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.6.2.tar.gz && \
    tar -xvzf openfst-1.6.2.tar.gz && \
    cd openfst-1.6.2/ && \
    ./configure --enable-static --enable-shared --enable-far --enable-ngram-fsts && \
    make -j $(nproc) && \
    make install && \
    cd


# Set environment variable for OpenFST
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib:/usr/local/lib/fst


# Download and build Phonetisaurus
RUN git clone https://github.com/AdolfVonKleist/Phonetisaurus.git && \
    cd Phonetisaurus && \
    ./configure && \
    make -j $(nproc) && \
    make install && \
    cd


RUN git clone https://github.com/mitlm/mitlm.git && \
    cd mitlm/ && \
    ./autogen.sh && \
    make -j $(nproc) && \
    make install && \
    cd

ADD worker/data-preparation-worker/src /data_prep_worker/
ADD shared/minio_communication.py  /data_prep_worker/
ADD shared/connector/ /data_prep_worker/connector/
ADD shared/wait-for.sh /tools/wait-for.sh

CMD ["python", "-u", "/data_prep_worker/data_preparation.py"]
