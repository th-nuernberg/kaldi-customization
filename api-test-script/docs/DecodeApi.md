# openapi_client.DecodeApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_decode_result**](DecodeApi.md#get_decode_result) | **GET** /project/{project_uuid}/training/{training_version}/decode/{decode_uuid} | Get the result of a decoding task
[**get_decodings**](DecodeApi.md#get_decodings) | **GET** /project/{project_uuid}/training/{training_version}/decode | List of all decodings
[**start_decode**](DecodeApi.md#start_decode) | **POST** /project/{project_uuid}/training/{training_version}/decode | Decode audio to text


# **get_decode_result**
> DecodeMessage get_decode_result(project_uuid, training_version, decode_uuid)

Get the result of a decoding task

Returns the result of a decoding task

### Example

* OAuth Authentication (oauth):
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
configuration = openapi_client.Configuration()
# Configure OAuth2 access token for authorization: oauth
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Defining host is optional and default to http://localhost:8080/api/v1
configuration.host = "http://localhost:8080/api/v1"
# Create an instance of the API class
api_instance = openapi_client.DecodeApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
decode_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the decoding task

try:
    # Get the result of a decoding task
    api_response = api_instance.get_decode_result(project_uuid, training_version, decode_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_decode_result: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **decode_uuid** | [**str**](.md)| UUID of the decoding task | 

### Return type

[**DecodeMessage**](DecodeMessage.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result of the decoding task |  -  |
**204** | Decoding not yet completed |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |
**415** | Unsupported media type |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_decodings**
> list[DecodeMessage] get_decodings(project_uuid, training_version)

List of all decodings

Returns a list of all decodings for this training version

### Example

* OAuth Authentication (oauth):
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
configuration = openapi_client.Configuration()
# Configure OAuth2 access token for authorization: oauth
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Defining host is optional and default to http://localhost:8080/api/v1
configuration.host = "http://localhost:8080/api/v1"
# Create an instance of the API class
api_instance = openapi_client.DecodeApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # List of all decodings
    api_response = api_instance.get_decodings(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_decodings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

[**list[DecodeMessage]**](DecodeMessage.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of decoding messages |  -  |
**400** | Training not finished |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_decode**
> DecodeTaskReference start_decode(project_uuid, training_version, audio_file)

Decode audio to text

Decode audio data to text using the trained project

### Example

* OAuth Authentication (oauth):
```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint
configuration = openapi_client.Configuration()
# Configure OAuth2 access token for authorization: oauth
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Defining host is optional and default to http://localhost:8080/api/v1
configuration.host = "http://localhost:8080/api/v1"
# Create an instance of the API class
api_instance = openapi_client.DecodeApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
audio_file = '/path/to/file' # file | Audio file for decoding

try:
    # Decode audio to text
    api_response = api_instance.start_decode(project_uuid, training_version, audio_file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->start_decode: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **audio_file** | **file**| Audio file for decoding | 

### Return type

[**DecodeTaskReference**](DecodeTaskReference.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Decoding successfully queued |  -  |
**400** | Training not finished |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

