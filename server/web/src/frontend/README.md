# Frontend

This is the frontend (and its server) to interact with the Kaldi Customization API. The frontend uses [Angular](https://angular.io/), [TypeScript](https://www.typescriptlang.org/) and [Less](http://lesscss.org/).

## Development Server

For faster development there is a development server, which can be executed on the host system and supports hot reloading.
This means, that a code file changed on disk, triggers the development server to rebuild the affected modules and perform a hot reload afterwards.

To start the development server follow the instructions below.
The frontend, can be accessed through [localhost:4200](http://localhost:4200/).

```bash
npm install -g @angular/cli@7.3.8

# install required dependencies to build swagger-client library
npm install --only=dev
npm run build:swagger-client

# install required dependencies (including swagger-client)
# to build the Kaldi Customization Frontend
npm install

# build and start the development server
npm run start
```

*Docker Compose has to be running, when using the development server.*

The API Server has to be accessable through [localhost:8080/api/](http://localhost:8080/api/).

## Production Server

The production server uses minimization and prerendering for better performance. It is used in the `web` container from the top-level `docker-compose.yaml`.

Follow the steps below to build and start the production server.

```bash
npm install -g @angular/cli@7.3.8

# install required dependencies to build swagger-client library
npm install --only=dev
npm run build:swagger-client

# install required dependencies (including swagger-client)
# to build the Kaldi Customization Frontend
npm install

# build and start the production server
npm run build:prod
npm run server
```

*Docker Compose has to be running, when using the production server.*

The API Server has to be accessable through [localhost:8080/api/](http://localhost:8080/api/).

### Reduce Required Disk Space

On the target system (e.g. Docker container), minimize the required disk space, by removing the `node_modules` directory and only install the modules required in production mode.

```bash
# only keep production dependencies
rm -rf node_modules
npm install --only=prod
```

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.
