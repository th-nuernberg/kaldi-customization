# openapi_client.UserApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](UserApi.md#create_user) | **POST** /user | Create user
[**get_user**](UserApi.md#get_user) | **GET** /user | Get current user
[**login_user**](UserApi.md#login_user) | **PUT** /user/login | Logs user into the system
[**logout_user**](UserApi.md#logout_user) | **POST** /user/logout/{token} | Logs out current logged in user session


# **create_user**
> create_user(user)

Create user

This can only be done by the logged in user.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.UserApi()
user = openapi_client.User() # User | Created user object

try:
    # Create user
    api_instance.create_user(user)
except ApiException as e:
    print("Exception when calling UserApi->create_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User**](User.md)| Created user object | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | successfully created |  -  |
**400** | Error at operation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user**
> User get_user()

Get current user

Provides info about the logged in user.

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
api_instance = openapi_client.UserApi(openapi_client.ApiClient(configuration))

try:
    # Get current user
    api_response = api_instance.get_user()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**403** | No user is logged in. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_user**
> str login_user(email, password)

Logs user into the system

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.UserApi()
email = 'email_example' # str | The user name for login
password = 'password_example' # str | The password for login in clear text

try:
    # Logs user into the system
    api_response = api_instance.login_user(email, password)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->login_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email** | **str**| The user name for login | 
 **password** | **str**| The password for login in clear text | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | successful operation |  * X-Rate-Limit - calls per hour allowed by the user <br>  * X-Expires-After - date in UTC when token expires <br>  |
**400** | Invalid username/password supplied |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout_user**
> logout_user(token)

Logs out current logged in user session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = openapi_client.UserApi()
token = '550e8400-e29b-11d4-a716-446655440000' # str | Access token to revoke

try:
    # Logs out current logged in user session
    api_instance.logout_user(token)
except ApiException as e:
    print("Exception when calling UserApi->logout_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | [**str**](.md)| Access token to revoke | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | successful operation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

