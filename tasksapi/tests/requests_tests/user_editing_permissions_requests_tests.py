"""Contains tests for user editing permissions."""

from rest_framework import status
from rest_framework.test import APITestCase
from .utils import (
    TEST_CONTAINER_TASK_TYPE_DICT,
    TEST_EXECUTABLE_TASK_TYPE_DICT,
)

# Put info about our fixtures data as constants here
NON_ADMIN_USER_AUTH_TOKEN = "02d205bc79d5e8f15f83e249ac227ef0085f953f"
NOT_USERS_CONTAINER_TASK_TYPE_PK = 1
NOT_USERS_EXECUTABLE_TASK_TYPE_PK = 1
NOT_USERS_QUEUE_PK = 1


class UserEditPermissionsRequestsTests(APITestCase):
    """Test user editing permissions."""

    fixtures = ["test-fixture.yaml"]

    def setUp(self):
        """Add in user's auth to client."""
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + NON_ADMIN_USER_AUTH_TOKEN
        )

    def test_modifying_other_users_container_task_type(self):
        """Test modifying another user's container task type."""
        put_response = self.client.put(
            "/api/containertasktypes/%d/" % NOT_USERS_CONTAINER_TASK_TYPE_PK,
            TEST_CONTAINER_TASK_TYPE_DICT,
            format="json",
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modifying_other_users_executable_task_type(self):
        """Test modifying another user's executable task type."""
        put_response = self.client.put(
            "/api/executabletasktypes/%d/" % NOT_USERS_EXECUTABLE_TASK_TYPE_PK,
            TEST_EXECUTABLE_TASK_TYPE_DICT,
            format="json",
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modifying_other_users_queue(self):
        """Test modifying another user's queue."""
        put_response = self.client.put(
            "/api/taskqueues/%d/" % NOT_USERS_QUEUE_PK,
            dict(name="mine now"),
            format="json",
        )

        self.assertEqual(put_response.status_code, status.HTTP_403_FORBIDDEN)
