# pspring-aws

This framework is member of pspring based family of frameworks. It provides a means to access aws resources with minimal code. `boto3` library is used internally for http requests.

All the default variables are listed in defaultvars.py

Annotations / Decorators that come along with this framework are listed below

* `@SecretValue(name="",region="",column="",columns=[])`
  
  This is a class decorator can be used to retrieve value of secret in AWS secrets manager. We could also specify a list of columns or a single column name from the secret response to be retrived. A method named "getSecretValue" will be available on the class.  
  
* `@DynamoDBTable(tableName="",primaryKey="",sortKey="",ttlColumnName="",ttl="")`
  
  This is a class decorator which can be tagged with a dynamodb table. Once tagged with this decorator, the class will have implementations of `get` and `put` methods.
  `get(self,primaryKey,sortKey="",columns="",column="")` method can be used to retrive only specific columns
  `put(self,data)` can be used to insert data
  
* `@LambdaHandler(type="lambdaproxy")`
  
  This is a class decorator which provides below functionalities. You should implement "handler" method which will be enhanced
  1) debug,info,warn,error - This will log a message will required tracking fields like requestId etc.
  2) handle cold start requests with requestId = "COLD_START_WARMER"
  3) addToLogger method can be used to add a field to all logging messages.
  4) returns a 200 response along with the dictionary returned from the "handler" method as json.
  5) handles all exceptions and returns gracefully a 500 Internal server error.


Below exceptions are available from this framework

- LambdaException
- NotFoundException
- UnAuthorizedException
- InternalServerException
- CreatedException
- RedirectException

* `RealTimeSecretsMgrConfigProvider`

  This along with https://github.com/vasudevan-palani/appsync-client.git works as a real time secrets manager ( what this means is, you will get notified about the changes to secrets mngr's value as a push event )

  ```python
    from pspring import Configuration

    config = Configuration.getConfig(__name__)

    Configuration.initializer([
      RealTimeSecretsMgrConfigProvider(secretId="mysecretId",region="us-east-1")
    ])

  ```

* `SecretsMgrConfigProvider`

  ConfigurationProvider for secrets manager in aws to work alongside pspring.Configuration
  
  ```python
      from pspring import Configuration

      config = Configuration.getConfig(__name__)

      Configuration.initializer([
        SecretsMgrConfigProvider(secretId="mysecretId",region="us-east-1")
      ])

    ```


* `SecretsManager`

  Utility class to interact with aws secrets manager encapsulating the boiler plate code
  ```python
    from pspringaws import SecretsManager

    secretsmngr = SecretsManager(secretId="mysecretId")

    secretsmngr.getSecretValue()

  ```

* `DynamoDBTable`

  Utility class to interact with aws dynamodb encapsulating the boiler plate code
  ```python
    from pspringaws import DynamoDBTable

    secretsmngr = DynamoDBTable(tableName="mytable",primaryKey="primaryKey",sortKey="sortKey")

    item = secretsmngr.get("primaryKeyValue")

    item = secretsmngr.put(primaryKeyValue,item)

  ```

Example:

```python

from pspring import *
from pspringaws import *


@LambdaHandler()
class MyHandler():
    @Autowired()
    def __init__(self,customerbackend:CustomerBackend, cache:DataCache):
        self.customerbackend = customerbackend
        self.cache = cache
        
    def handler(self,event,context):
      return self.customerbackend(...)

context.initialize()
newhandler = MyHandler()
def handler(event,context):
    return newhandler.handler(event,context)
```

 To do:
 
 * Support Lambda integration types
