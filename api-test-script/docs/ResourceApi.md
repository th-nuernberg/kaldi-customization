# openapi_client.ResourceApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**assign_resource_to_training**](ResourceApi.md#assign_resource_to_training) | **POST** /project/{project_uuid}/training/{training_version}/resource | Assign a resource to the training
[**create_resource**](ResourceApi.md#create_resource) | **POST** /resource | Create/Upload a new resource
[**delete_assigned_resource_from_training**](ResourceApi.md#delete_assigned_resource_from_training) | **DELETE** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid} | Remove a resource from the training
[**get_corpus_of_training_resource**](ResourceApi.md#get_corpus_of_training_resource) | **GET** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/corpus | Get the corpus of the resource
[**get_resource**](ResourceApi.md#get_resource) | **GET** /resource | Returns a list of available resources
[**get_resource_by_uuid**](ResourceApi.md#get_resource_by_uuid) | **GET** /resource/{resource_uuid} | Find resource by UUID
[**get_resource_data**](ResourceApi.md#get_resource_data) | **GET** /resource/{resource_uuid}/data | Returns the resource content
[**set_corpus_of_training_resource**](ResourceApi.md#set_corpus_of_training_resource) | **PUT** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/corpus | Set the corpus of the resource


# **assign_resource_to_training**
> Resource assign_resource_to_training(project_uuid, training_version, resource_reference_object=resource_reference_object)

Assign a resource to the training

Assign the specified resource to the training

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
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_reference_object = openapi_client.ResourceReferenceObject() # ResourceReferenceObject | Resource that needs to be added (optional)

try:
    # Assign a resource to the training
    api_response = api_instance.assign_resource_to_training(project_uuid, training_version, resource_reference_object=resource_reference_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourceApi->assign_resource_to_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **resource_reference_object** | [**ResourceReferenceObject**](ResourceReferenceObject.md)| Resource that needs to be added | [optional] 

### Return type

[**Resource**](Resource.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Resource successfully assigned |  -  |
**400** | Resource already in training |  -  |
**403** | Forbidden |  -  |
**404** | Project, training or resource not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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
**202** | Upload successful |  -  |
**403** | Forbidden |  -  |
**405** | Invalid input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_assigned_resource_from_training**
> delete_assigned_resource_from_training(project_uuid, training_version, resource_uuid)

Remove a resource from the training

Removes the assigned resource from the training

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
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource

try:
    # Remove a resource from the training
    api_instance.delete_assigned_resource_from_training(project_uuid, training_version, resource_uuid)
except ApiException as e:
    print("Exception when calling ResourceApi->delete_assigned_resource_from_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **resource_uuid** | [**str**](.md)| UUID of the resource | 

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
**200** | Resource assignment successfully removed |  -  |
**403** | Forbidden |  -  |
**404** | Project, training or resource not found |  -  |
**409** | Conflict: already in training |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_corpus_of_training_resource**
> str get_corpus_of_training_resource(project_uuid, training_version, resource_uuid)

Get the corpus of the resource

Returns the corpus of the specified resource for this training

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
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource

try:
    # Get the corpus of the resource
    api_response = api_instance.get_corpus_of_training_resource(project_uuid, training_version, resource_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResourceApi->get_corpus_of_training_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **resource_uuid** | [**str**](.md)| UUID of the resource | 

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
**200** | Corpus as plain text |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

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

# **set_corpus_of_training_resource**
> set_corpus_of_training_resource(project_uuid, training_version, resource_uuid, body)

Set the corpus of the resource

Updates the corpus of the specified resource for this training

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
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource
body = 'body_example' # str | New or updated corpus as plain text

try:
    # Set the corpus of the resource
    api_instance.set_corpus_of_training_resource(project_uuid, training_version, resource_uuid, body)
except ApiException as e:
    print("Exception when calling ResourceApi->set_corpus_of_training_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **resource_uuid** | [**str**](.md)| UUID of the resource | 
 **body** | **str**| New or updated corpus as plain text | 

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: text/plain
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |
**409** | Training already started |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

