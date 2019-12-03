FROM python:3.7-alpine3.9
LABEL maintainer="@dinomite94"

RUN mkdir /test_text_prep_worker/ && \
    mkdir /tools/ && \
    mkdir /test_text_prep_worker/test-files

ADD worker/text-preparation-worker/requirements.txt /test_text_prep_worker/requirements.txt
WORKDIR /test_text_prep_worker

RUN apk update && \
    apk upgrade && \
    apk add build-base libffi-dev openssl-dev tesseract-ocr-data-deu zlib-dev libxml2-dev \
            libjpeg-turbo-dev libxslt-dev poppler-utils --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD worker/text-preparation-worker/test/src/ /test_text_prep_worker/
ADD shared/minio_communication.py /test_text_prep_worker/
ADD shared/connector/ /test_text_prep_worker/connector/
ADD shared/wait-for.sh /tools/wait-for.sh

CMD ["python", "-u", "/test_text_prep_worker/test_text_preparation.py"]
