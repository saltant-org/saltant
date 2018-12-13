"""Import tests here so Django notices them."""

# Comment out any tests you don't want to run
from .model_tests import TasksApiModelTests
from .container_execution_tests import ContainerExecutionTests
from .executable_execution_tests import ExecutableExecutionTests
from .request_tests import TasksApiBasicHTTPRequestsTests
