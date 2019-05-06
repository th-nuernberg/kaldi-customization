FROM python:3.7-alpine3.9
MAINTAINER Tobias Kruse <***REMOVED***>

EXPOSE 5000
VOLUME ["/www/data"]

ADD requirements.txt /www/requirements.txt
WORKDIR /www

RUN apk add build-base libffi-dev openssl-dev --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD src /www
ADD run.sh /www

CMD ["/bin/sh", "-c", "/www/run.sh"]
