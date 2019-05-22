FROM python:3.7-alpine3.9
MAINTAINER Tobias Kruse <***REMOVED***>

EXPOSE 5000
VOLUME ["/www/asr", "/www/texts"]

ADD requirements.txt /www/requirements.txt
WORKDIR /www

RUN apk add build-base libffi-dev openssl-dev mariadb-connector-c-dev --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD src /www
ADD wait-for.sh /tools/wait-for.sh

ENV FLASK_APP=/www/app.py

CMD ["/bin/sh", "/tools/wait-for.sh", "db:3306", "--", "python", "-m", "flask", "run", "--host=0.0.0.0"]
