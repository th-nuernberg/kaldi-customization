FROM python:3.7-alpine3.9
MAINTAINER Tobias Kruse <***REMOVED***>

EXPOSE 5000
VOLUME ["/www/data"]

ADD requirements.txt /www/requirements.txt
WORKDIR /www

RUN apk add build-base libffi-dev openssl-dev mariadb-connector-c-dev --no-cache && \
    pip install -r requirements.txt && \
    apk del build-base

ADD src /www

ENV FLASK_APP=/www/app.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
