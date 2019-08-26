# openapi_client.DecodeApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_audio_by_uuid**](DecodeApi.md#delete_audio_by_uuid) | **DELETE** /audio/{audio_uuid} | Delete audio by UUID
[**get_all_audio**](DecodeApi.md#get_all_audio) | **GET** /audio | Returns a list of available audio
[**get_audio_by_uuid**](DecodeApi.md#get_audio_by_uuid) | **GET** /audio/{audio_uuid} | Find audio by UUID
[**get_audio_data**](DecodeApi.md#get_audio_data) | **GET** /audio/{audio_uuid}/data | Returns the audio content
[**get_decode_result**](DecodeApi.md#get_decode_result) | **GET** /project/{project_uuid}/training/{training_version}/decode/{decode_uuid} | Get the result of a decoding task
[**get_decodings**](DecodeApi.md#get_decodings) | **GET** /project/{project_uuid}/training/{training_version}/decode | List of all decodings
[**start_decode**](DecodeApi.md#start_decode) | **POST** /project/{project_uuid}/training/{training_version}/decode | Decode audio to text
[**upload_audio**](DecodeApi.md#upload_audio) | **POST** /audio | Uploads audio


# **delete_audio_by_uuid**
> delete_audio_by_uuid(audio_uuid)

Delete audio by UUID

Delete a single audio resource

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
audio_uuid = 'audio_uuid_example' # str | UUID of audio to delete

try:
    # Delete audio by UUID
    api_instance.delete_audio_by_uuid(audio_uuid)
except ApiException as e:
    print("Exception when calling DecodeApi->delete_audio_by_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audio_uuid** | **str**| UUID of audio to delete | 

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**403** | Forbidden |  -  |
**404** | Audio not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_audio**
> list[Audio] get_all_audio()

Returns a list of available audio

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

try:
    # Returns a list of available audio
    api_response = api_instance.get_all_audio()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_all_audio: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Audio]**](Audio.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of resources |  -  |
**403** | Forbidden |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_audio_by_uuid**
> Audio get_audio_by_uuid(audio_uuid)

Find audio by UUID

Returns a single audio resource

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
audio_uuid = 'audio_uuid_example' # str | UUID of audio to return

try:
    # Find audio by UUID
    api_response = api_instance.get_audio_by_uuid(audio_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_audio_by_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audio_uuid** | **str**| UUID of audio to return | 

### Return type

[**Audio**](Audio.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Audio object |  -  |
**403** | Forbidden |  -  |
**404** | Audio not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_audio_data**
> file get_audio_data(audio_uuid)

Returns the audio content

Returns the audio content

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
audio_uuid = 'audio_uuid_example' # str | UUID of resource to return

try:
    # Returns the audio content
    api_response = api_instance.get_audio_data(audio_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_audio_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audio_uuid** | **str**| UUID of resource to return | 

### Return type

**file**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: audio/wav

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Uploaded audio content |  -  |
**403** | Forbidden |  -  |
**404** | Audio not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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
> DecodeTaskReference start_decode(project_uuid, training_version, audio_reference_object)

Decode audio to text

Decode audio data to text using the trained project and the given audio

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
audio_reference_object = openapi_client.AudioReferenceObject() # AudioReferenceObject | Audio that needs to be decoded

try:
    # Decode audio to text
    api_response = api_instance.start_decode(project_uuid, training_version, audio_reference_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->start_decode: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **audio_reference_object** | [**AudioReferenceObject**](AudioReferenceObject.md)| Audio that needs to be decoded | 

### Return type

[**DecodeTaskReference**](DecodeTaskReference.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Decoding successfully queued |  -  |
**400** | Training not finished |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_audio**
> Audio upload_audio(upfile)

Uploads audio

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
upfile = '/path/to/file' # file | File object that needs to be uploaded

try:
    # Uploads audio
    api_response = api_instance.upload_audio(upfile)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->upload_audio: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upfile** | **file**| File object that needs to be uploaded | 

### Return type

[**Audio**](Audio.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of resources |  -  |
**403** | Forbidden |  -  |
**405** | Invalid Input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

