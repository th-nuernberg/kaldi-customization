FROM python:3.7-alpine3.9
LABEL maintainer="***REMOVED***"

RUN mkdir /test_worker/ && \
    mkdir /tools/ && \
    mkdir /test_worker/test-files

ADD worker/test-worker/requirements.txt /test_worker/requirements.txt
WORKDIR /test_worker

RUN apk update && \
    apk upgrade && \
    apk add build-base && \
    pip install -r requirements.txt && \
    apk del build-base

ADD worker/test-worker/src/ /test_worker/
ADD shared/minio_communication.py /test_worker/
ADD shared/test-files/ /test_worker/test-files/
ADD shared/wait-for.sh /tools/wait-for.sh

CMD ["/bin/sh", "/test_worker/test-worker.sh"]
