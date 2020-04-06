FROM kaldi-base

ADD shared/connector/requirements.txt /opt/kaldi/connector/requirements.txt

RUN pip3 install -r /opt/kaldi/connector/requirements.txt

ADD shared/connector /opt/kaldi/connector
ADD worker/kaldi-worker/worker.py /opt/kaldi/worker.py
ADD shared/wait-for.sh /opt/tools/wait-for.sh
ADD shared/minio_communication.py /opt/kaldi/minio_communication.py
ADD shared/redis_config.py /opt/kaldi/redis_config.py
ADD worker/kaldi-worker/scripts /opt/kaldi/scripts

CMD ["python3", "-u", "/opt/kaldi/worker.py"]
