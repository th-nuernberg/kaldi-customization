FROM alpine:3.7
LABEL maintainer="@toksicon"

ARG KALDI_ARGS=--shared


COPY tools/extras/srilm-1.7.2.tar.gz /tmp/srilm.tgz

# Install deps
RUN apk add --no-cache --update \
            bash \
            gawk \
            linux-headers \
            build-base \
            gfortran \
            git \
            subversion \
            zlib-dev \
            libexecinfo \
            libexecinfo-dev \
            automake \
            autoconf \
            libtool \
            perl \
            python2 \
            python3 \
            sox \
            tar \
            libstdc++ \
            libgfortran

RUN git clone https://github.com/kaldi-asr/kaldi.git /kaldi --depth=1
RUN cd /kaldi/tools && make -j$(nproc) openblas && make -j$(nproc)
RUN cd /kaldi/src && export LDLIBS='-lexecinfo' && \
    ./configure $KALDI_ARGS --openblas-root=../tools/OpenBLAS/install && \ 
    make -j$(nproc)

RUN apk add file tar gzip && cp /tmp/srilm.tgz /kaldi/tools/srilm.tgz && \
	cd /kaldi/tools/ && ./install_srilm.sh && \
	rm /tmp/srilm.tgz && rm /kaldi/tools/srilm.tgz

RUN apk del -y \
            linux-headers \
            build-base \
            gfortran \
            git \
            subversion \
            zlib-dev \
            libexecinfo-dev \
            automake \
            autoconf \
            libtool \
            python2 && \
    rm -rf /var/cache/apk/* && \
    rm -rf /kaldi/.git /kaldi/egs /kaldi/misc /kaldi/scripts /kaldi/windows .git* .travis.yml && \
    find /kaldi/src/ -type f \( -not -name '*.so' -and -not -name '*.so*' -and -not -name '*.sh' -and -not -perm /u=x,g=x,o=x \) -delete && \
    find /kaldi/tools/ -type f \( -not -name '*.so' -and -not -name '*.so*' -and -not -name '*.sh' -and -not -perm /u=x,g=x,o=x \) -delete && \
    ln -s /usr/bin/python3 /usr/bin/python


CMD ["/bin/bash"]
