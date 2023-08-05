# Getting started

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=BATester%20with%20custom%20parameters-Python)


## How to Use

The following section explains how to use the Batesterwithcustomparameters SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=BATester%20with%20custom%20parameters-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=BATester%20with%20custom%20parameters-Python&projectName=batesterwithcustomparamdemov1)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=BATester%20with%20custom%20parameters-Python&projectName=batesterwithcustomparamdemov1)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=BATester%20with%20custom%20parameters-Python&projectName=batesterwithcustomparamdemov1)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from batesterwithcustomparamdemov1.batesterwithcustomparamdemov_1_client import Batesterwithcustomparamdemov1Client
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=BATester%20with%20custom%20parameters-Python&libraryName=batesterwithcustomparamdemov1.batesterwithcustomparamdemov_1_client&projectName=batesterwithcustomparamdemov1&className=Batesterwithcustomparamdemov1Client)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=BATester%20with%20custom%20parameters-Python&libraryName=batesterwithcustomparamdemov1.batesterwithcustomparamdemov_1_client&projectName=batesterwithcustomparamdemov1&className=Batesterwithcustomparamdemov1Client)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| username | TODO: add a description |
| password | TODO: add a description |



API client can be initialized as following.

```python
# Configuration parameters and credentials
username = 'farhan'
password = 'apimatic'

client = Batesterwithcustomparamdemov1Client(username, password)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [APIController](#api_controller)

## <a name="api_controller"></a>![Class: ](https://apidocs.io/img/class.png ".APIController") APIController

### Get controller instance

An instance of the ``` APIController ``` class can be accessed from the API Client.

```python
 client_controller = client.client
```

### <a name="get_basic_auth_test"></a>![Method: ](https://apidocs.io/img/method.png ".APIController.get_basic_auth_test") get_basic_auth_test

> TODO: Add a method description

```python
def get_basic_auth_test(self)
```

#### Example Usage

```python

result = client_controller.get_basic_auth_test()

```


[Back to List of Controllers](#list_of_controllers)



