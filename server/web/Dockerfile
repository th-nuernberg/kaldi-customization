FROM node:8.15.1-alpine
LABEL maintainer="Tobias Kruse <***REMOVED***>"

EXPOSE 4200


ADD src /www

WORKDIR /www/frontend
RUN npm install -g @angular/cli@7.3.8
RUN npm install
RUN npm run build:prod
RUN rm -rf node_modules
RUN npm install --only=prod

CMD ["npm", "run", "server", "--host", "0.0.0.0", "--disable-host-check"]
