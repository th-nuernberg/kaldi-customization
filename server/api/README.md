# Kaldi Customization API Server

Tasks:
 * Connects frontend/workers and database
 * Connects frontend and workers
 * Handles uploads and manages files in MinIO for workers
 * Provides files to download for the frontend
 * Sends tasks to task queues in Redis
 * Handles authentication

## Structure

The app is located in the `src` directory. Under that directory there are the following parts.

### `db`
Contains the database models implemented in [SQLAlchemy](http://sqlalche.me/).

### `swagger`
Sources generated by the [Swagger Codegen](https://swagger.io/tools/swagger-codegen/).
 * Sources in `swagger/controllers` and `swagger/models` may have been modified to implement required logic. Therefore it is recommended to use a merge tool (e.g. [Meld](https://meldmerge.org/)) to update these sources with newer generated sources.
 * A copy of the current API definition has to be placed in `swagger/swagger/kaldi-customization.json`. This is used by the [Swagger UI](https://swagger.io/tools/swagger-ui/) available at the URL `<host>/api/v1/docs/`.