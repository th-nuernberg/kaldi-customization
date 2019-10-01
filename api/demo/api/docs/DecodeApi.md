# openapi_client.DecodeApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**assign_audio_to_current_session**](DecodeApi.md#assign_audio_to_current_session) | **POST** /project/{project_uuid}/training/{training_version}/decode | Assign Audio to decoding session
[**create_decode_session**](DecodeApi.md#create_decode_session) | **POST** /project/{project_uuid}/training/{training_version}/decode/session | Create a new decoding session
[**delete_audio_by_uuid**](DecodeApi.md#delete_audio_by_uuid) | **DELETE** /audio/{audio_uuid} | Delete audio by UUID
[**delete_decode_session**](DecodeApi.md#delete_decode_session) | **DELETE** /project/{project_uuid}/training/{training_version}/decode/session | Delete the decoding session
[**get_all_audio**](DecodeApi.md#get_all_audio) | **GET** /audio | Returns a list of available audio
[**get_all_decode_sessions**](DecodeApi.md#get_all_decode_sessions) | **GET** /project/{project_uuid}/training/{training_version}/decode/session | Get the all sessions
[**get_audio_by_uuid**](DecodeApi.md#get_audio_by_uuid) | **GET** /audio/{audio_uuid} | Find audio by UUID
[**get_audio_data**](DecodeApi.md#get_audio_data) | **GET** /audio/{audio_uuid}/data | Returns the audio content
[**get_current_decode_session**](DecodeApi.md#get_current_decode_session) | **GET** /project/{project_uuid}/training/{training_version}/decode/session/current | Get the current session
[**get_decode_result**](DecodeApi.md#get_decode_result) | **GET** /project/{project_uuid}/training/{training_version}/decode/{audio_uuid} | Get the result of a decoding task
[**get_decode_session**](DecodeApi.md#get_decode_session) | **GET** /project/{project_uuid}/training/{training_version}/decode/session/{session_uuid} | Get a decode session
[**get_decodings**](DecodeApi.md#get_decodings) | **GET** /project/{project_uuid}/training/{training_version}/decode | List of all decodings
[**start_decode**](DecodeApi.md#start_decode) | **PUT** /project/{project_uuid}/training/{training_version}/decode/session/{session_uuid}/commit | Commits the decode session for decoding
[**unassign_audio_to_current_session**](DecodeApi.md#unassign_audio_to_current_session) | **DELETE** /project/{project_uuid}/training/{training_version}/decode/{audio_uuid} | Unassign Audio to decoding session
[**upload_audio**](DecodeApi.md#upload_audio) | **POST** /audio | Uploads audio


# **assign_audio_to_current_session**
> DecodeAudio assign_audio_to_current_session(project_uuid, training_version, audio_reference_object)

Assign Audio to decoding session

Assign audio to current decoding session

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
    # Assign Audio to decoding session
    api_response = api_instance.assign_audio_to_current_session(project_uuid, training_version, audio_reference_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->assign_audio_to_current_session: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **audio_reference_object** | [**AudioReferenceObject**](AudioReferenceObject.md)| Audio that needs to be decoded | 

### Return type

[**DecodeAudio**](DecodeAudio.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Audio successfully added to session |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found or no active session |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_decode_session**
> DecodeSession create_decode_session(project_uuid, training_version)

Create a new decoding session

Create a new decoding session

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
    # Create a new decoding session
    api_response = api_instance.create_decode_session(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->create_decode_session: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

[**DecodeSession**](DecodeSession.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The new active DecodeSession |  -  |
**400** | An active session already exists |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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

# **delete_decode_session**
> delete_decode_session(project_uuid, training_version)

Delete the decoding session

Delete the active decoding session

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
    # Delete the decoding session
    api_instance.delete_decode_session(project_uuid, training_version)
except ApiException as e:
    print("Exception when calling DecodeApi->delete_decode_session: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

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
**200** | Session deleted |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found or no active decoding session |  -  |

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

# **get_all_decode_sessions**
> list[DecodeSession] get_all_decode_sessions(project_uuid, training_version)

Get the all sessions

Get the current decode session

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
    # Get the all sessions
    api_response = api_instance.get_all_decode_sessions(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_all_decode_sessions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

[**list[DecodeSession]**](DecodeSession.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The decode session for this training |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

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

# **get_current_decode_session**
> DecodeSession get_current_decode_session(project_uuid, training_version)

Get the current session

Get the current decode session

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
    # Get the current session
    api_response = api_instance.get_current_decode_session(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_current_decode_session: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

[**DecodeSession**](DecodeSession.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The active DecodeSession |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found or session not started |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_decode_result**
> DecodeAudio get_decode_result(project_uuid, training_version, audio_uuid)

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
audio_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the audio

try:
    # Get the result of a decoding task
    api_response = api_instance.get_decode_result(project_uuid, training_version, audio_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_decode_result: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **audio_uuid** | [**str**](.md)| UUID of the audio | 

### Return type

[**DecodeAudio**](DecodeAudio.md)

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

# **get_decode_session**
> DecodeSession get_decode_session(project_uuid, training_version, session_uuid)

Get a decode session

Gets a specified session

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
session_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the session

try:
    # Get a decode session
    api_response = api_instance.get_decode_session(project_uuid, training_version, session_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->get_decode_session: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **session_uuid** | [**str**](.md)| UUID of the session | 

### Return type

[**DecodeSession**](DecodeSession.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The queried decode session |  -  |
**403** | Forbidden |  -  |
**404** | Project, training or session not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_decodings**
> list[DecodeAudio] get_decodings(project_uuid, training_version)

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

[**list[DecodeAudio]**](DecodeAudio.md)

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
> DecodeSession start_decode(project_uuid, training_version, session_uuid, callback_object=callback_object)

Commits the decode session for decoding

Enqueue the currently active session for decoding

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
session_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the session
callback_object = openapi_client.CallbackObject() # CallbackObject | Callbackobject that gets executed after process (optional)

try:
    # Commits the decode session for decoding
    api_response = api_instance.start_decode(project_uuid, training_version, session_uuid, callback_object=callback_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DecodeApi->start_decode: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **session_uuid** | [**str**](.md)| UUID of the session | 
 **callback_object** | [**CallbackObject**](CallbackObject.md)| Callbackobject that gets executed after process | [optional] 

### Return type

[**DecodeSession**](DecodeSession.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Session successfully commited |  -  |
**400** | Training not finished or session already in progress |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unassign_audio_to_current_session**
> unassign_audio_to_current_session(project_uuid, training_version, audio_uuid)

Unassign Audio to decoding session

Unassign audio to current decoding session

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
audio_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the audio

try:
    # Unassign Audio to decoding session
    api_instance.unassign_audio_to_current_session(project_uuid, training_version, audio_uuid)
except ApiException as e:
    print("Exception when calling DecodeApi->unassign_audio_to_current_session: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **audio_uuid** | [**str**](.md)| UUID of the audio | 

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
**201** | Audio successfully unassigned from session |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found or no active session or audio not in active session |  -  |

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
**201** | Created Resource |  -  |
**403** | Forbidden |  -  |
**405** | Invalid Input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

