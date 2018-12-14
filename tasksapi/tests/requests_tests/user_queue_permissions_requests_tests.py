"""Contains tests for user queue permissions."""

from rest_framework import status
from rest_framework.test import APITestCase

# Put info about our fixtures data as constants here
NON_ADMIN_USER_AUTH_TOKEN = "02d205bc79d5e8f15f83e249ac227ef0085f953f"
NOT_USERS_PRIVATE_QUEUE_PK = 3
PUBLIC_INACTIVE_QUEUE_PK = 2
CONTAINER_TASK_TYPE_PK = 1
EXECUTABLE_TASK_TYPE_PK = 1


class UserQueuePermissionsRequestsTests(APITestCase):
    """Test user queue permissions."""

    fixtures = ["test-fixture.yaml"]

    def setUp(self):
        """Add in user's auth to client."""
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + NON_ADMIN_USER_AUTH_TOKEN
        )

    def test_posting_to_inactive_queue(self):
        """Test posting a job to an inactive queue."""
        post_response_1 = self.client.post(
            "/api/containertaskinstances/",
            dict(
                name="my-task-instance",
                task_type=CONTAINER_TASK_TYPE_PK,
                task_queue=PUBLIC_INACTIVE_QUEUE_PK,
            ),
            format="json",
        )
        post_response_2 = self.client.post(
            "/api/executabletaskinstances/",
            dict(
                name="my-task-instance",
                task_type=EXECUTABLE_TASK_TYPE_PK,
                task_queue=PUBLIC_INACTIVE_QUEUE_PK,
            ),
            format="json",
        )

        self.assertEqual(
            post_response_1.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            post_response_2.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_posting_to_other_users_private_queue(self):
        """Test posting a job to another user's private queue."""
        post_response_1 = self.client.post(
            "/api/containertaskinstances/",
            dict(
                name="my-task-instance",
                task_type=CONTAINER_TASK_TYPE_PK,
                task_queue=NOT_USERS_PRIVATE_QUEUE_PK,
            ),
            format="json",
        )
        post_response_2 = self.client.post(
            "/api/executabletaskinstances/",
            dict(
                name="my-task-instance",
                task_type=EXECUTABLE_TASK_TYPE_PK,
                task_queue=NOT_USERS_PRIVATE_QUEUE_PK,
            ),
            format="json",
        )

        self.assertEqual(
            post_response_1.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            post_response_2.status_code, status.HTTP_400_BAD_REQUEST
        )
