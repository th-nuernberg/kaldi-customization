FROM python:2.7-alpine3.10
VOLUME ["/data_prep_worker/in", "/data_prep_worker/out"]
WORKDIR /data-preparation-worker


ADD src/data_preparation.py /data-preparation-worker/ 
ADD src/minio_communication.py /data-preparation-worker/ 
ADD src/data_processing.py /data-preparation-worker/
ADD wait-for.sh /data-preparation-worker/ 
ADD requirements.txt /data-preparation-worker/


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


# Download and build Phonetisaurus
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

CMD ["/bin/sh", "/data-preparation-worker/wait-for.sh", "redis:6379", "--", "python", "-u", "/data-preparation-worker/data_preparation.py"]
