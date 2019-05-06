FROM node:8.15.1-alpine
MAINTAINER Tobias Kruse <***REMOVED***>

EXPOSE 4200


ADD src /www

WORKDIR /www/frontend
RUN npm install -g @angular/cli && npm install

CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
