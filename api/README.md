# Kaldi Customization API

## API Definition (`openapi.yaml`)

The `openapi.yaml` file contains the [OpenAPI 3](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) API definition for the communication between the Kaldi Customization API server and clients, used by the web frontend and the workflow demo.

The generator uses this file to generate the server and client code. The *clients are fully functional* and can be replaced with a newly generated client library by *overriding* it.

As the generated *server only contains empty function bodies*, it is required to *merge* the newly generated code with the already existing implementation of the server. 


## Generate a new API Server and Clients (`generate.py`, `generator/`)

Execute the `generate.py` script to generate the Python API Server and a Python client for the workflow demo and a TypeScript client for the frontend.

```python3 generate.py``` *or* ```python generate.py``` (assuming `python(.exe)` is Python 3)

Enter the `out` directory, then:

 * Copy `python_client/*` into `kaldi-customization/api/demo`
 * Copy `typescript_client/*` into `kaldi-customization/server/web/src/frontend/projects/swagger-client/src`
    * **Fix `test/plain` responses** (see Known Issues below)
 * Merge `server/openapi_server` into `kaldi-customization/server/api/src/openapi_server`


## API Workflow Demo (`demo/`)

Contains a sample workflow using the generated Python API client (on `http://localhost:8080/api/v1`):
 * Create Project
 * Create Training
 * Upload Resources
 * Assign Resources to Training
 * Start Training
 * Decode Audio Files with Trained Model


## Known Issues

### Type `File` (Generator Bug)
A defined type named `File` is generated to `java.io.File` in Python imports.

**Solution:** Do not define a type named `File`

### Responses of Content Type `text/plain` (Generator Bug)
A generated TypeScript client tries to parse responses of content type `text/plain` as JSON.

**Solution:**

Modify the methods with a `text/plain` response ...

```
// to determine the Accept header
const httpHeaderAccepts: string[] = [
    'text/plain'
];
```

..., to expect a plain string, and not a JSON string:

```
// Generated Example:
return this.httpClient.get<string>(`<uri>`,
    {
        withCredentials: this.configuration.withCredentials,
        headers: headers,
        observe: observe,
        reportProgress: reportProgress
    }
);
```

1. Remove template parameter `<string>` from the `httpClient` request
2. Add property `responseType: 'text'` to the `httpClient` options

```
// Fixed Example:
return this.httpClient.get(`<uri>`,
    {
        withCredentials: this.configuration.withCredentials,
        headers: headers,
        observe: observe,
        reportProgress: reportProgress,
        responseType: 'text'
    }
);
```
