# Kaldi Customization API

## API Definition (`openapi.yaml`)

The `openapi.yaml` file contains the [OpenAPI 3](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md) API definition for the communication between the Kaldi Customization API server and clients, used by the web frontend and the workflow demo.

The generator uses this file to generate the server and client code. The *clients are fully functional* and can be replaced with a newly generated client library by *overriding* it.

As the generated *server only contains empty function bodies*, it is required to *merge* the newly generated code with the already existing implementation of the server. 


# How to change the API

There are several steps to make changes to the API!

1) **Customize interface** <br> 
    Make the desired change in the yaml-file in
    ```
    kaldi-customization/api/openapi.yaml
    ```
2) **CleanUp of old generated files** <br>
    It is urgently necessary to delete the old generated files to ensure a new clean generation. <br>
    The following folders must be deleted:
    ```
    kaldi-customization/api/out
    kaldi-customization/api/tools
    ```
3) **Generate new interface** <br>
    Run python-file to generate new interface:
    ```
    kaldi-customization/api/generate.py
    ```
4) **Check & merge server logic** <br>
    After generating the new interface, you need to check the differences of all files that contain server-logic in:
    ```
    generated:              kaldi-customization/api/out/server/openapi_server
    existing server-logic:  kaldi-customization/server/api/src/openapi_server
    ```
    Merge the generated new functions into the server-logic. <br>
    *Diff- and merge-tools of an IDEA like PYCharm can assist you.*
    
5) **Update server-interface** <br>
    Apply the interface definition for the server:
    ```
    new def.:       kaldi-customization/api/openapi.yaml
    server def.:    kaldi-customization/server/api/src/openapi_server/openapi/openapi.yaml
    ```
   



# Generate a new API Server and Clients (`generate.py`, `generator/`)

Execute the `generate.py` script to generate the Python API Server and a Python client for the workflow demo and a TypeScript client for the frontend.

```python3 generate.py``` *or* ```python generate.py``` (assuming `python(.exe)` is Python 3)

## Clients

The clients are moved to the destinations in `kaldi-customization/api/demo/api` and `kaldi-customization/server/web/src/frontend/projects/swagger-client/src` automatically.

## Server

As previous mentioned, it is not possible to override the API server. A manual merge of the newly generated code from `out/server/opernapi_server` into the existing code in `kaldi-customization/server/api/src/openapi_server` is required.

To have a look what changed, the `python3 generator/diff.py` script can be executed. It displays the operation changes (diff of the `openapi.yaml` files) and the generated function call changes (diff of the `<tag>_controller.py` files).

*Nevertheless, it is highly recommended to use a merge tool to perform the API server update.*


# API Workflow Demo (`demo/`)

Contains a sample workflow using the generated Python API client (on `http://localhost:8080/api/v1`):
 * Create Project
 * Create Training
 * Upload Resources
 * Assign Resources to Training
 * Start Training
 * Decode Audio Files with Trained Model


# Known Issues

## Type `File` (OpenAPI Generator Bug)
A defined type named `File` is generated to `java.io.File` in Python imports.

**Solution:**  
Do not define a type named `File`

## Required Positional Argument (OpenAPI Generator Bug)
A positional argument has no default value, but will be set in the function body, if no value is passed by the caller.

```
if connexion.request.is_json:
    <argument> = <Object>.from_dict(connexion.request.get_json())  # noqa: E501
```

**Solution:**  
Add a default value `<argument>=None` to the concerned positional argument in the argument list manually.

## Responses of Content Type `text/plain` (OpenAPI Generator Bug)
A generated TypeScript client tries to parse responses of content type `text/plain` as JSON.

**Solution:**

*The solution is implemented in the generator script (`generator/typescript_angular.py`) and does not require any manual handling.*

The script modifies the methods in `out/typescript_client/api/*.service.ts` with a `text/plain` response ...

```
// to determine the Accept header
const httpHeaderAccepts: string[] = [
    'text/plain'
];
```

..., to expect a plain string, and not a JSON string:

```
// OpenAPI Generated Example:
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
