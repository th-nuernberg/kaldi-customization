FROM node:8.15.1-alpine
LABEL maintainer="Tobias Kruse <***REMOVED***>"

EXPOSE 4200


ADD src /www

WORKDIR /www/frontend
RUN npm install -g @angular/cli@7.3.8

# install required dependencies to build swagger-client library
RUN npm install --only=dev && \
    npm install @angular/common@~7.2.0 rxjs@~6.3.3
RUN ng build swagger-client

# build the frontend
RUN npm install
RUN npm run build:prod

# only keep production dependencies
RUN rm -rf node_modules
RUN npm install --only=prod

CMD ["npm", "run", "server", "--host", "0.0.0.0", "--disable-host-check"]
