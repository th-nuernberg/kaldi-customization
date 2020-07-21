# openapi_client.TrainingApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**assign_resource_to_training**](TrainingApi.md#assign_resource_to_training) | **POST** /project/{project_uuid}/training/{training_version}/resource | Assign a resource to the training
[**create_training**](TrainingApi.md#create_training) | **POST** /project/{project_uuid}/training | Create a new training
[**delete_assigned_resource_from_training**](TrainingApi.md#delete_assigned_resource_from_training) | **DELETE** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid} | Remove a resource from the training
[**download_model_for_training**](TrainingApi.md#download_model_for_training) | **GET** /project/{project_uuid}/training/{training_version}/model | Returns the model
[**get_corpus_of_training**](TrainingApi.md#get_corpus_of_training) | **GET** /project/{project_uuid}/training/{training_version}/corpus | Get the entire corpus of the specified training
[**get_corpus_of_training_resource**](TrainingApi.md#get_corpus_of_training_resource) | **GET** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/corpus | Get the corpus of the resource
[**get_current_training_for_project**](TrainingApi.md#get_current_training_for_project) | **GET** /project/{project_uuid}/training/current | Get current training
[**get_lexicon_of_training**](TrainingApi.md#get_lexicon_of_training) | **GET** /project/{project_uuid}/training/{training_version}/lexicon | Get the entire lexicon of the specified training
[**get_lexicon_of_training_resource**](TrainingApi.md#get_lexicon_of_training_resource) | **GET** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/lexicon | Get the lexicon of the resource
[**get_training_by_version**](TrainingApi.md#get_training_by_version) | **GET** /project/{project_uuid}/training/{training_version} | Find project training results by UUID
[**get_trainings_for_project**](TrainingApi.md#get_trainings_for_project) | **GET** /project/{project_uuid}/training | Lists all Trainings of a Project
[**get_vocabulary_of_training**](TrainingApi.md#get_vocabulary_of_training) | **GET** /project/{project_uuid}/training/{training_version}/vocabulary | Get the entire vocabulary of the specified training
[**prepare_training_by_version**](TrainingApi.md#prepare_training_by_version) | **PUT** /project/{project_uuid}/training/{training_version}/prepare | Prepare the specified training
[**set_corpus_of_training_resource**](TrainingApi.md#set_corpus_of_training_resource) | **PUT** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/corpus | Set the corpus of the resource
[**set_lexicon_of_training_resource**](TrainingApi.md#set_lexicon_of_training_resource) | **PUT** /project/{project_uuid}/training/{training_version}/resource/{resource_uuid}/lexicon | Set the lexicon of the resource
[**start_training_by_version**](TrainingApi.md#start_training_by_version) | **PUT** /project/{project_uuid}/training/{training_version}/train | Start the specified training


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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_reference_object = openapi_client.ResourceReferenceObject() # ResourceReferenceObject | Resource that needs to be added (optional)

try:
    # Assign a resource to the training
    api_response = api_instance.assign_resource_to_training(project_uuid, training_version, resource_reference_object=resource_reference_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->assign_resource_to_training: %s\n" % e)
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

# **create_training**
> Training create_training(project_uuid)

Create a new training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | Project object that needs to be trained

try:
    # Create a new training
    api_response = api_instance.create_training(project_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->create_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| Project object that needs to be trained | 

### Return type

[**Training**](Training.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | created successfully |  -  |
**403** | Forbidden |  -  |
**404** | Project not found |  -  |

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource

try:
    # Remove a resource from the training
    api_instance.delete_assigned_resource_from_training(project_uuid, training_version, resource_uuid)
except ApiException as e:
    print("Exception when calling TrainingApi->delete_assigned_resource_from_training: %s\n" % e)
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

# **download_model_for_training**
> file download_model_for_training(project_uuid, training_version)

Returns the model

Returns the model of the specified training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = 'project_uuid_example' # str | UUID of project
training_version = 56 # int | Version of training

try:
    # Returns the model
    api_response = api_instance.download_model_for_training(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->download_model_for_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | **str**| UUID of project | 
 **training_version** | **int**| Version of training | 

### Return type

**file**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/zip

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Trained model content |  -  |
**403** | Forbidden |  -  |
**404** | Page not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_corpus_of_training**
> str get_corpus_of_training(project_uuid, training_version)

Get the entire corpus of the specified training

Returns the entire corpus of the specified training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Get the entire corpus of the specified training
    api_response = api_instance.get_corpus_of_training(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_corpus_of_training: %s\n" % e)
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
**200** | Corpus as plain text |  -  |
**400** | Training not prepared |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource

try:
    # Get the corpus of the resource
    api_response = api_instance.get_corpus_of_training_resource(project_uuid, training_version, resource_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_corpus_of_training_resource: %s\n" % e)
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

# **get_current_training_for_project**
> Training get_current_training_for_project(project_uuid)

Get current training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | Get the current training for a specific project

try:
    # Get current training
    api_response = api_instance.get_current_training_for_project(project_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_current_training_for_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| Get the current training for a specific project | 

### Return type

[**Training**](Training.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The current training |  -  |
**403** | Forbidden |  -  |
**404** | Project or Training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_lexicon_of_training**
> list[list[str]] get_lexicon_of_training(project_uuid, training_version)

Get the entire lexicon of the specified training

Returns the entire lexicon of the specified training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Get the entire lexicon of the specified training
    api_response = api_instance.get_lexicon_of_training(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_lexicon_of_training: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

**list[list[str]]**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Lexicon as array with string-pairs |  -  |
**400** | Training not prepared |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_lexicon_of_training_resource**
> list[list[str]] get_lexicon_of_training_resource(project_uuid, training_version, resource_uuid)

Get the lexicon of the resource

Returns the lexicon of the specified resource for this training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource

try:
    # Get the lexicon of the resource
    api_response = api_instance.get_lexicon_of_training_resource(project_uuid, training_version, resource_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_lexicon_of_training_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **resource_uuid** | [**str**](.md)| UUID of the resource | 

### Return type

**list[list[str]]**

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Lexicon as array with string-pairs |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_training_by_version**
> Training get_training_by_version(project_uuid, training_version)

Find project training results by UUID

Returns the training object

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Find project training results by UUID
    api_response = api_instance.get_training_by_version(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_training_by_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 

### Return type

[**Training**](Training.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Got the specified training |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_trainings_for_project**
> list[Training] get_trainings_for_project(project_uuid)

Lists all Trainings of a Project

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | Get all trainings for a specific project

try:
    # Lists all Trainings of a Project
    api_response = api_instance.get_trainings_for_project(project_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_trainings_for_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| Get all trainings for a specific project | 

### Return type

[**list[Training]**](Training.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | all trainings |  -  |
**403** | Forbidden |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vocabulary_of_training**
> str get_vocabulary_of_training(project_uuid, training_version)

Get the entire vocabulary of the specified training

Returns the entire vocabulary of the specified training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project

try:
    # Get the entire vocabulary of the specified training
    api_response = api_instance.get_vocabulary_of_training(project_uuid, training_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->get_vocabulary_of_training: %s\n" % e)
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
**200** | Vocabulary as line-separated plain text |  -  |
**400** | Training not prepared |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **prepare_training_by_version**
> Training prepare_training_by_version(project_uuid, training_version, callback_object=callback_object)

Prepare the specified training

Start the preparation process for the specified training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
callback_object = openapi_client.CallbackObject() # CallbackObject | Callback to be executed after the operation ended (optional)

try:
    # Prepare the specified training
    api_response = api_instance.prepare_training_by_version(project_uuid, training_version, callback_object=callback_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->prepare_training_by_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **callback_object** | [**CallbackObject**](CallbackObject.md)| Callback to be executed after the operation ended | [optional] 

### Return type

[**Training**](Training.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Preparation successfully queued |  -  |
**400** | training already done or pending |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource
body = 'body_example' # str | New or updated corpus as plain text

try:
    # Set the corpus of the resource
    api_instance.set_corpus_of_training_resource(project_uuid, training_version, resource_uuid, body)
except ApiException as e:
    print("Exception when calling TrainingApi->set_corpus_of_training_resource: %s\n" % e)
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

# **set_lexicon_of_training_resource**
> set_lexicon_of_training_resource(project_uuid, training_version, resource_uuid, request_body)

Set the lexicon of the resource

Updates the lexicon of the specified resource for this training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
resource_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the resource
request_body = None # list[list[str]] | New or updated lexicon as array with string-pairs

try:
    # Set the lexicon of the resource
    api_instance.set_lexicon_of_training_resource(project_uuid, training_version, resource_uuid, request_body)
except ApiException as e:
    print("Exception when calling TrainingApi->set_lexicon_of_training_resource: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **resource_uuid** | [**str**](.md)| UUID of the resource | 
 **request_body** | [**list[list[str]]**](list.md)| New or updated lexicon as array with string-pairs | 

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

# **start_training_by_version**
> Training start_training_by_version(project_uuid, training_version, callback_object=callback_object)

Start the specified training

Start the training process for the specified training

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
api_instance = openapi_client.TrainingApi(openapi_client.ApiClient(configuration))
project_uuid = '550e8400-e29b-11d4-a716-446655440000' # str | UUID of the project
training_version = 56 # int | Training version of the project
callback_object = openapi_client.CallbackObject() # CallbackObject | Callback to be executed after the operation ended (optional)

try:
    # Start the specified training
    api_response = api_instance.start_training_by_version(project_uuid, training_version, callback_object=callback_object)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TrainingApi->start_training_by_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_uuid** | [**str**](.md)| UUID of the project | 
 **training_version** | **int**| Training version of the project | 
 **callback_object** | [**CallbackObject**](CallbackObject.md)| Callback to be executed after the operation ended | [optional] 

### Return type

[**Training**](Training.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Training successfully queued |  -  |
**400** | training already done or pending |  -  |
**403** | Forbidden |  -  |
**404** | Project or training not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

