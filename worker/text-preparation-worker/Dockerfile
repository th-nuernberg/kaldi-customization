FROM python:3.7-alpine3.9
LABEL maintainer="@dinomite94"

RUN mkdir /text_prep_worker/ && \
    mkdir /text_prep_worker/in/ && \
    mkdir /text_prep_worker/out/ && \
    mkdir /tools/

ADD worker/text-preparation-worker/requirements.txt /text_prep_worker/requirements.txt
WORKDIR /text_prep_worker

RUN apk update && \
    apk upgrade && \
    apk add build-base libffi-dev openssl-dev tesseract-ocr-data-deu zlib-dev libxml2-dev \
            libjpeg-turbo-dev libxslt-dev poppler-utils --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD worker/text-preparation-worker/src/ /text_prep_worker/
ADD shared/minio_communication.py /text_prep_worker/
ADD shared/connector/ /text_prep_worker/connector/
ADD shared/wait-for.sh /tools/wait-for.sh

CMD ["python", "-u", "/text_prep_worker/text_preparation.py"]
