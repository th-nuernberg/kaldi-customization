FROM toksicon/kaldi-base:latest
LABEL maintainer="***REMOVED***"

ADD shared/connector/requirements.txt /kaldi/connector/requirements.txt

RUN pip3 install -r /kaldi/connector/requirements.txt

ADD shared/connector /kaldi/connector
ADD worker/decode-worker/worker.py /kaldi/worker.py
ADD shared/wait-for.sh /tools/wait-for.sh
ADD shared/minio_communication.py /kaldi/minio_communication.py
ADD shared/redis_config.py /kaldi/redis_config.py
ADD worker/decode-worker/scripts /kaldi/scripts

CMD ["python3", "-u", "/kaldi/worker.py"]
