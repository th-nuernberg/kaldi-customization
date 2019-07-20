FROM kaldi-base
LABEL maintainer="Tobias Kruse <***REMOVED***>"

ADD shared/connector/requirements.txt /kaldi/connector/requirements.txt

RUN pip3 install -r /kaldi/connector/requirements.txt

ADD shared/connector /kaldi/connector
ADD worker/kaldi-worker/worker.py /kaldi/worker.py
ADD shared/wait-for.sh /tools/wait-for.sh
ADD shared/minio_communication.py /kaldi/minio_communication.py
ADD shared/redis_config.py /kaldi/redis_config.py
ADD worker/kaldi-worker/scripts /kaldi/scripts

CMD ["python3", "-u", "/kaldi/worker.py"]
