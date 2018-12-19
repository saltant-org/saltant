"""Contains tests for basic API requests."""

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase
from tasksapi.constants import PUBLISHED
from tasksapi.models import User
from .utils import (
    TEST_CONTAINER_TASK_TYPE_DICT,
    TEST_EXECUTABLE_TASK_TYPE_DICT,
    TEST_TASK_QUEUE_DICT,
    TEST_TASK_WHITELIST_DICT,
)

# The user and their password used in these tests
USER_USERNAME = "AzureDiamond"
USER_PASSWORD = "hunter2"


class BasicHTTPRequestsTests(APITransactionTestCase):
    """Test basic HTTP requests.

    I.e., GET, POST, and PUT for most models. Nothing fancy here
    exploring permissions.
    """

    # Ensure the PKs get reset after each test
    reset_sequences = True

    def setUp(self):
        """Generate the user used by the tests."""
        self.user = User(username=USER_USERNAME)
        self.user.set_password(USER_PASSWORD)
        self.user.save()

    def http_requests_barrage(self):
        """Fire a barrage of HTTP requests at the API.
        """
        # POST, GET, and PUT a container task type
        post_response = self.client.post(
            "/api/containertasktypes/",
            TEST_CONTAINER_TASK_TYPE_DICT,
            format="json",
        )
        get_response_1 = self.client.get(
            "/api/containertasktypes/", format="json"
        )
        get_response_2 = self.client.get(
            "/api/containertasktypes/1/", format="json"
        )
        put_response = self.client.put(
            "/api/containertasktypes/1/",
            {**TEST_CONTAINER_TASK_TYPE_DICT, "name": "different"},
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PUT an executable task type. "true" doesn't
        # really do anything, but I guess that's ideal for a test?
        post_response = self.client.post(
            "/api/executabletasktypes/",
            TEST_EXECUTABLE_TASK_TYPE_DICT,
            format="json",
        )
        get_response_1 = self.client.get(
            "/api/executabletasktypes/", format="json"
        )
        get_response_2 = self.client.get(
            "/api/executabletasktypes/1/", format="json"
        )
        put_response = self.client.put(
            "/api/executabletasktypes/1/",
            {**TEST_EXECUTABLE_TASK_TYPE_DICT, "name": "different"},
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PUT a task whitelist.
        post_response = self.client.post(
            "/api/taskwhitelists/", TEST_TASK_WHITELIST_DICT, format="json"
        )
        get_response_1 = self.client.get("/api/taskwhitelists/", format="json")
        get_response_2 = self.client.get(
            "/api/taskwhitelists/1/", format="json"
        )
        put_response = self.client.put(
            "/api/taskwhitelists/1/",
            {**TEST_TASK_WHITELIST_DICT, "name": "different"},
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PUT a task queue
        post_response = self.client.post(
            "/api/taskqueues/", TEST_TASK_QUEUE_DICT, format="json"
        )
        get_response_1 = self.client.get("/api/taskqueues/", format="json")
        get_response_2 = self.client.get("/api/taskqueues/1/", format="json")
        put_response = self.client.put(
            "/api/taskqueues/1/",
            {**TEST_TASK_QUEUE_DICT, "name": "different"},
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PATCH a container task instance
        post_response = self.client.post(
            "/api/containertaskinstances/",
            dict(
                name="my-task-instance",
                task_type=1,
                task_queue=1,
                arguments={"name": "Daniel"},
            ),
            format="json",
        )

        # Get the UUID of the task instance we just made
        new_uuid = post_response.data["uuid"]

        # Continue with the requests
        get_response_1 = self.client.get(
            "/api/containertaskinstances/", format="json"
        )
        get_response_2 = self.client.get(
            "/api/containertaskinstances/" + new_uuid + "/", format="json"
        )
        patch_response = self.client.patch(
            "/api/updatetaskinstancestatus/" + new_uuid + "/",
            dict(state=PUBLISHED),
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Now let's test the clone and terminate endpoints for task
        # instances
        clone_response = self.client.post(
            "/api/containertaskinstances/" + new_uuid + "/clone/",
            format="json",
        )

        new_uuid = clone_response.data["uuid"]

        terminate_response = self.client.post(
            "/api/containertaskinstances/" + new_uuid + "/terminate/",
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(clone_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            terminate_response.status_code, status.HTTP_202_ACCEPTED
        )

        # POST, GET, and PATCH an executable task instance
        post_response = self.client.post(
            "/api/executabletaskinstances/",
            dict(
                name="my-task-instance",
                task_type=1,
                task_queue=1,
                arguments={"name": "Daniel"},
            ),
            format="json",
        )

        # Get the UUID of the task instance we just made
        new_uuid = post_response.data["uuid"]

        # Continue with the requests
        get_response_1 = self.client.get(
            "/api/executabletaskinstances/", format="json"
        )
        get_response_2 = self.client.get(
            "/api/executabletaskinstances/" + new_uuid + "/", format="json"
        )
        patch_response = self.client.patch(
            "/api/updatetaskinstancestatus/" + new_uuid + "/",
            dict(state=PUBLISHED),
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Now let's test the clone and terminate endpoints for task
        # instances
        clone_response = self.client.post(
            "/api/executabletaskinstances/" + new_uuid + "/clone/",
            format="json",
        )

        new_uuid = clone_response.data["uuid"]

        terminate_response = self.client.post(
            "/api/executabletaskinstances/" + new_uuid + "/terminate/",
            format="json",
        )

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(clone_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            terminate_response.status_code, status.HTTP_202_ACCEPTED
        )

    def test_basic_http_requests_token_auth(self):
        """Make sure basic HTTP requests work using token authentication."""
        # Create an authentication token
        token = Token.objects.create(user=self.user)

        # Authenticate with the auth token we made
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Run tests
        self.http_requests_barrage()

    def test_basic_http_requests_jwt_auth(self):
        """Make sure basic HTTP requests work using JWT authentication."""
        # Get a JWT access token and use it
        jwt_response = self.client.post(
            "/api/token/",
            dict(username=USER_USERNAME, password=USER_PASSWORD),
            format="json",
        )
        access_token = jwt_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # Run tests
        self.http_requests_barrage()

    def test_basic_http_requests_session_auth(self):
        """Make sure basic HTTP requests work using session authentication."""
        # Authenticate with a session
        self.client.login(username=USER_USERNAME, password=USER_PASSWORD)

        # Run tests
        self.http_requests_barrage()

        # Log out of the session
        self.client.logout()
