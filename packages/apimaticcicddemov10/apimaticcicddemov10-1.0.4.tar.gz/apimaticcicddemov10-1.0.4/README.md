# Getting started

Simple calculator API hosted on APIMATIC

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=APIMATIC%20Calculator-Python)


## How to Use

The following section explains how to use the Apimaticcalculator SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=APIMATIC%20Calculator-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=APIMATIC%20Calculator-Python&projectName=apimaticcicddemov10)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=APIMATIC%20Calculator-Python&projectName=apimaticcicddemov10)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=APIMATIC%20Calculator-Python&projectName=apimaticcicddemov10)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from apimaticcicddemov10.apimaticcicddemov_10_client import Apimaticcicddemov10Client
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=APIMATIC%20Calculator-Python&libraryName=apimaticcicddemov10.apimaticcicddemov_10_client&projectName=apimaticcicddemov10&className=Apimaticcicddemov10Client)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=APIMATIC%20Calculator-Python&libraryName=apimaticcicddemov10.apimaticcicddemov_10_client&projectName=apimaticcicddemov10&className=Apimaticcicddemov10Client)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### 

API client can be initialized as following.

```python

client = Apimaticcicddemov10Client()
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [SimpleCalculatorController](#simple_calculator_controller)

## <a name="simple_calculator_controller"></a>![Class: ](https://apidocs.io/img/class.png ".SimpleCalculatorController") SimpleCalculatorController

### Get controller instance

An instance of the ``` SimpleCalculatorController ``` class can be accessed from the API Client.

```python
 simple_calculator_controller = client.simple_calculator
```

### <a name="get_ci_cd_demo_for_calculator"></a>![Method: ](https://apidocs.io/img/method.png ".SimpleCalculatorController.get_ci_cd_demo_for_calculator") get_ci_cd_demo_for_calculator

> Calculates the expression using the specified operation.

```python
def get_ci_cd_demo_for_calculator(self,
                                      options=dict())
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| operation |  ``` Required ```  | The operator to apply on the variables |
| x |  ``` Required ```  | The LHS value |
| y |  ``` Required ```  | The RHS value |



#### Example Usage

```python
collect = {}

operation = OperationTypeEnum.MULTIPLY
collect['operation'] = operation

x = 4
collect['x'] = x

y = 5
collect['y'] = y


result = simple_calculator_controller.get_ci_cd_demo_for_calculator(collect)

```


[Back to List of Controllers](#list_of_controllers)



