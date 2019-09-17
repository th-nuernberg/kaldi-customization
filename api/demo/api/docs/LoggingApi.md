# openapi_client.LoggingApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_perparation_log**](LoggingApi.md#get_perparation_log) | **GET** /project/{project_uuid}/training/{training_version}/prepare/log | Get Training Log
[**get_resource_log**](LoggingApi.md#get_resource_log) | **GET** /resource/{resource_uuid}/log | Find resource by UUID
[**get_training_log**](LoggingApi.md#get_training_log) | **GET** /project/{project_uuid}/training/{training_version}/train/log | Get Training Log
[**get_training_stats**](LoggingApi.md#get_training_stats) | **GET** /project/{project_uuid}/training/{training_version}/stats | Get Training Stats


# **get_perparation_log**
> str get_perparation_log(project_uuid, training_version)

Get Training Log

Returns the log of a preparation

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
api_instance = openapi_client.LoggingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Get Training Log
    api_response = api_instance.get_perparation_log(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoggingApi->get_perparation_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

**str**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | log as plain text |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource_log**
> str get_resource_log(resource_uuid)

Find resource by UUID

Returns the log of a resource

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
api_instance = openapi_client.LoggingApi(openapi_client.ApiClient(configuration))
resource_uuid = 'resource_uuid_example' # str | UUID of resource to return

try:
    # Find resource by UUID
    api_response = api_instance.get_resource_log(resource_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoggingApi->get_resource_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_uuid** | **str**| UUID of resource to return | 

### Return type

**str**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | log as plain text |  -  |
**403** | Forbidden |  -  |
**404** | Page not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_training_log**
> str get_training_log(project_uuid, training_version)

Get Training Log

Returns the log of a training

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
api_instance = openapi_client.LoggingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Get Training Log
    api_response = api_instance.get_training_log(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoggingApi->get_training_log: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

**str**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | log as plain text |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_training_stats**
> DataPrepStats get_training_stats(project_uuid, training_version)

Get Training Stats

Returns the stats to be reviewed before training

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
api_instance = openapi_client.LoggingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Get Training Stats
    api_response = api_instance.get_training_stats(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoggingApi->get_training_stats: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

[**DataPrepStats**](DataPrepStats.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Stats for this training |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

