"""Import tests here so Django notices them."""

# Comment out any tests you don't want to run
from .container_execution_tests import TasksApiContainerTests
from .executable_execution_tests import TasksApiExecutableTests
from .model_tests import TasksApiModelTests
from .request_tests import TasksApiBasicHTTPRequestsTests
