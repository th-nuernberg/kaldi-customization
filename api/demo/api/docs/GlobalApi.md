# openapi_client.GlobalApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_acoustic_model**](GlobalApi.md#download_acoustic_model) | **GET** /global/acoustic_models/{acoustic_model_uuid}/model | Returns the acoustic model
[**get_acoustic_models**](GlobalApi.md#get_acoustic_models) | **GET** /global/acoustic_models | Returns a list of available acoustic models
[**get_languages**](GlobalApi.md#get_languages) | **GET** /global/languages | Returns a list of available languages


# **download_acoustic_model**
> file download_acoustic_model(acoustic_model_uuid)

Returns the acoustic model

Returns the model of the specified acoustic model

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.GlobalApi()
acoustic_model_uuid = 'acoustic_model_uuid_example' # str | UUID of the acoustic model

try:
    # Returns the acoustic model
    api_response = api_instance.download_acoustic_model(acoustic_model_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GlobalApi->download_acoustic_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **acoustic_model_uuid** | **str**| UUID of the acoustic model | 

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Acoustic Model |  -  |
**403** | Forbidden |  -  |
**404** | Page not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_acoustic_models**
> list[AcousticModel] get_acoustic_models()

Returns a list of available acoustic models

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.GlobalApi()

try:
    # Returns a list of available acoustic models
    api_response = api_instance.get_acoustic_models()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GlobalApi->get_acoustic_models: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[AcousticModel]**](AcousticModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of acoustic models |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_languages**
> list[Language] get_languages()

Returns a list of available languages

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.GlobalApi()

try:
    # Returns a list of available languages
    api_response = api_instance.get_languages()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GlobalApi->get_languages: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Language]**](Language.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of acoustic models |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

