FROM kaldi-base
LABEL maintainer="Tobias Kruse <***REMOVED***>"

ADD shared/connector/requirements.txt /kaldi/connector/requirements.txt

RUN pip3 install -r /kaldi/connector/requirements.txt

ADD shared/connector /kaldi/connector
ADD worker/kaldi-worker/worker.py /kaldi/worker.py
ADD shared/wait-for.sh /tools/wait-for.sh

ENTRYPOINT ["/bin/sh", "/tools/wait-for.sh", "minio:9000", "--", "/bin/sh", "/tools/wait-for.sh", "redis:6379", "--", "python3", "-u", "/kaldi/worker.py", "--redis-host=redis", "--redis-password=kalditproject", "--minio-host=minio"]
