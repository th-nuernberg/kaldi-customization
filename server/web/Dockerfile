FROM node:8.15.1-alpine
MAINTAINER Tobias Kruse <***REMOVED***>

EXPOSE 4200


ADD src /www

WORKDIR /www/frontend
RUN npm install -g @angular/cli && npm install --only=dev && npm build:prod && rm -rf node_modules && npm install --only=prod

CMD ["ng", "server", "--host", "0.0.0.0", "--disable-host-check"]
