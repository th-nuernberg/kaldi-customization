# openapi_client.ResourceApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_resource**](ResourceApi.md#create_resource) | **POST** /resource | Create/Upload a new resource
[**get_resource**](ResourceApi.md#get_resource) | **GET** /resource | Returns a list of available resources
[**get_resource_by_uuid**](ResourceApi.md#get_resource_by_uuid) | **GET** /resource/{resource_uuid} | Find resource by UUID
[**get_resource_data**](ResourceApi.md#get_resource_data) | **GET** /resource/{resource_uuid}/data | Returns the resource content


# **create_resource**
> Resource create_resource(upfile)

Create/Upload a new resource

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
api_instance = openapi_client.ResourceApi(openapi_client.ApiClient(configuration))
upfile = '/path/to/file' # file | File object that needs to be uploaded

try:
    # Create/Upload a new resource
    api_response = api_instance.create_resource(upfile)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourceApi->create_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upfile** | **file**| File object that needs to be uploaded | 

### Return type

[**Resource**](Resource.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Upload successful and preparation queued |  -  |
**403** | Forbidden |  -  |
**405** | Invalid input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource**
> list[Resource] get_resource()

Returns a list of available resources

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
api_instance = openapi_client.ResourceApi(openapi_client.ApiClient(configuration))

try:
    # Returns a list of available resources
    api_response = api_instance.get_resource()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourceApi->get_resource: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Resource]**](Resource.md)

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

# **get_resource_by_uuid**
> Resource get_resource_by_uuid(resource_uuid)

Find resource by UUID

Returns a single resource

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
api_instance = openapi_client.ResourceApi(openapi_client.ApiClient(configuration))
resource_uuid = 'resource_uuid_example' # str | UUID of resource to return

try:
    # Find resource by UUID
    api_response = api_instance.get_resource_by_uuid(resource_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourceApi->get_resource_by_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_uuid** | **str**| UUID of resource to return | 

### Return type

[**Resource**](Resource.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Resource object |  -  |
**403** | Forbidden |  -  |
**404** | Page not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource_data**
> file get_resource_data(resource_uuid)

Returns the resource content

Returns the resource content

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
api_instance = openapi_client.ResourceApi(openapi_client.ApiClient(configuration))
resource_uuid = 'resource_uuid_example' # str | UUID of resource to return

try:
    # Returns the resource content
    api_response = api_instance.get_resource_data(resource_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourceApi->get_resource_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_uuid** | **str**| UUID of resource to return | 

### Return type

**file**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf, image/png, text/html, text/plain, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Uploaded resource content |  -  |
**403** | Forbidden |  -  |
**404** | Page not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

