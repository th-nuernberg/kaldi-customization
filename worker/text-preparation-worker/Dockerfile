FROM python:3.7-alpine3.9
MAINTAINER Dino Pehratovic <***REMOVED***>

VOLUME ["/text_prep_worker/in", "/text_prep_worker/out"]

ADD requirements.txt /text_prep_worker/requirements.txt
WORKDIR /text_prep_worker

RUN apk add build-base libffi-dev openssl-dev tesseract-ocr-data-deu zlib-dev libxml2-dev --no-cache && \
    apk add libjpeg-turbo-dev libxslt-dev poppler-utils --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD src/text_preparation.py /text_prep_worker
ADD wait-for.sh /tools/wait-for.sh

CMD ["/bin/sh", "/tools/wait-for.sh", "redis:6379", "--", "python", "-u", "/text_prep_worker/text_preparation.py"]
