FROM node:8.15.1-alpine
MAINTAINER Tobias Kruse <***REMOVED***>

EXPOSE 4200


ADD src /www

WORKDIR /www/frontend
RUN npm install -g @angular/cli@7.3.8 && \
    npm install && \
    npm run build:prod && \
    rm -rf node_modules && \
    npm install --only=prod

CMD ["npm", "run", "server", "--host", "0.0.0.0", "--disable-host-check"]
