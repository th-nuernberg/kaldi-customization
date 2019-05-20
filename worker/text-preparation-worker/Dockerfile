FROM python:3.7-alpine3.9
MAINTAINER Dino Pehratovic <***REMOVED***>

VOLUME ["/text_prep_worker/in", "/text_prep_worker/out"]

ADD requirements.txt /text_prep_worker/requirements.txt
WORKDIR /text_prep_worker

RUN apk add build-base libffi-dev openssl-dev tesseract-ocr-data-deu zlib-dev libxml2-dev libjpeg-turbo-dev libxslt-dev --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD text_preparation.py /text_prep_worker

CMD ["python3", "/text_prep_worker/text_preparation.py"]
