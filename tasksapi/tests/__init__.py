"""Import tests here so Django notices them."""

# Comment out any tests you don't want to run
from .execution_tests.container_execution_tests import ContainerExecutionTests
from .execution_tests.executable_execution_tests import (
    ExecutableExecutionTests,
)
from .requests_tests.basic_requests_tests import BasicHTTPRequestsTests
from .requests_tests.user_editing_permissions_requests_tests import (
    UserEditPermissionsRequestsTests,
)
