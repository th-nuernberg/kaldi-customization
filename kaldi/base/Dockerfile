FROM kaldiasr/kaldi:latest


# add srilm
COPY srilm.tgz /opt/kaldi/tools/srilm.tgz

RUN apt-get -y install curl wget gawk && \
	cd /opt/kaldi/tools && \
    extras/install_srilm.sh

# set python3 as default, install pip

RUN ln -fs /usr/bin/python3 /usr/bin/python && \
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
	python get-pip.py

CMD ["/bin/bash"]
