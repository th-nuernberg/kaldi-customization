FROM python:3.7-alpine3.9
LABEL maintainer="Tobias Kruse <***REMOVED***>"

EXPOSE 5000

ADD server/api/requirements.txt /www/requirements.txt
ADD shared/connector/requirements.txt /www/connector/requirements.txt
WORKDIR /www

RUN apk add build-base libffi-dev openssl-dev mariadb-connector-c-dev --no-cache && \
    pip install -r requirements.txt && \
    pip install -r /www/connector/requirements.txt && \
    apk del build-base

ADD server/api/src /www
ADD shared/connector /www/connector
ADD shared/wait-for.sh /tools/wait-for.sh

ENV FLASK_APP=/www/app.py

CMD ["/bin/sh", "/tools/wait-for.sh", "db:3306", "--", "python", "-m", "flask", "run", "--host=0.0.0.0"]
