FROM python:3.7-alpine3.9
LABEL maintainer="@dinomite94"

RUN mkdir /test_data_prep_worker/ && \
    mkdir /opt/tools/

ADD worker/data-preparation-worker/requirements.txt /test_data_prep_worker/requirements.txt
WORKDIR /test_data_prep_worker

RUN apk update && \
    apk upgrade && \
    apk add build-base libffi-dev openssl-dev tesseract-ocr-data-deu zlib-dev libxml2-dev \
            libjpeg-turbo-dev libxslt-dev poppler-utils --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD worker/data-preparation-worker/test/src/ /test_data_prep_worker/
ADD shared/minio_communication.py /test_data_prep_worker/
ADD shared/wait-for.sh /opt/tools/wait-for.sh

CMD ["python", "-u", "/test_data_prep_worker/test_data_preparation.py"]
