"""Contains request tests for the tasksapi."""

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APIClient,
    APITransactionTestCase,)
from tasksapi.constants import (
    PUBLISHED,
    DOCKER,)


class TasksApiBasicHTTPRequestsTests(APITransactionTestCase):
    """Test HTTP requests."""
    # Ensure the PKs get reset after each test
    reset_sequences = True

    def http_requests_barrage(self, client):
        """Fire a barrage of HTTP requests at the API.

        Arg:
            client: A rest_framework.test.APIClient which has already
                been authenticated with the tasks API.
        """
        # POST, GET, and PUT a container task type
        post_response = client.post(
            '/api/containertasktypes/',
            dict(
                name='my-task-type',
                description="Fantastic task type",
                container_image='mwiens91/hello-world',
                container_type=DOCKER,
                command_to_run='/app/hello_world.py',
                logs_path='/logs/',
                results_path='/results/',
                environment_variables=['HOME'],
                required_arguments=['name'],
                required_arguments_default_values={'name': 'AzureDiamond'},),
            format='json',)
        get_response_1 = client.get(
            '/api/containertasktypes/',
            format='json',)
        get_response_2 = client.get(
            '/api/containertasktypes/1/',
            format='json',)
        put_response = client.put(
            '/api/containertasktypes/1/',
            dict(
                name='my-task-type',
                description="Fantastic task type 2",
                container_image='mwiens91/hello-world',
                container_type=DOCKER,
                command_to_run='/app/hello_world.py',
                logs_path='/logs/',
                results_path='/results/',
                environment_variables=['HOME'],
                required_arguments=['name'],
                required_arguments_default_values={'name': 'AzureDiamond'},),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PUT an executable task type. "true" doesn't
        # really do anything, but I guess that's ideal for a test?
        post_response = client.post(
            '/api/executabletasktypes/',
            dict(
                name='my-task-type',
                description="Fantastic task type",
                command_to_run='true',
                environment_variables=['HOME'],
                required_arguments=['name'],
                required_arguments_default_values={'name': 'AzureDiamond'},),
            format='json',)
        get_response_1 = client.get(
            '/api/executabletasktypes/',
            format='json',)
        get_response_2 = client.get(
            '/api/executabletasktypes/1/',
            format='json',)
        put_response = client.put(
            '/api/executabletasktypes/1/',
            dict(
                name='my-task-type',
                description="Fantastic task type 2",
                command_to_run='true',
                environment_variables=['HOME'],
                required_arguments=['name'],
                required_arguments_default_values={'name': 'AzureDiamond'},),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PUT a task queue
        post_response = client.post(
            '/api/taskqueues/',
            dict(
                name='my-task-queue',
                description="Fantastic task queue",
                private=False,
                active=True,),
            format='json',)
        get_response_1 = client.get(
            '/api/taskqueues/',
            format='json',)
        get_response_2 = client.get(
            '/api/taskqueues/1/',
            format='json',)
        put_response = client.put(
            '/api/taskqueues/1/',
            dict(
                name='my-task-queue',
                description="Fantastic task queue 2",
                private=False,
                active=True,),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PATCH a container task instance
        post_response = client.post(
            '/api/containertaskinstances/',
            dict(
                name='my-task-instance',
                task_type=1,
                task_queue=1,
                arguments={'name': 'Daniel'},),
            format='json',)

        # Get the UUID of the task instance we just made
        new_uuid = post_response.data['uuid']

        # Continue with the requests
        get_response_1 = client.get(
            '/api/containertaskinstances/',
            format='json',)
        get_response_2 = client.get(
            '/api/containertaskinstances/' + new_uuid + '/',
            format='json',)
        patch_response = client.patch(
            '/api/updatetaskinstancestatus/' + new_uuid + '/',
            dict(state=PUBLISHED,),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Now let's test the clone and terminate endpoints for task
        # instances
        clone_response = client.post(
            '/api/containertaskinstances/' + new_uuid + '/clone/',
            format='json',)

        new_uuid = clone_response.data['uuid']

        terminate_response = client.post(
            '/api/containertaskinstances/' + new_uuid + '/terminate/',
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(clone_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            terminate_response.status_code,
            status.HTTP_202_ACCEPTED)

        # POST, GET, and PATCH an executable task instance
        post_response = client.post(
            '/api/executabletaskinstances/',
            dict(
                name='my-task-instance',
                task_type=1,
                task_queue=1,
                arguments={'name': 'Daniel'},),
            format='json',)

        # Get the UUID of the task instance we just made
        new_uuid = post_response.data['uuid']

        # Continue with the requests
        get_response_1 = client.get(
            '/api/executabletaskinstances/',
            format='json',)
        get_response_2 = client.get(
            '/api/executabletaskinstances/' + new_uuid + '/',
            format='json',)
        patch_response = client.patch(
            '/api/updatetaskinstancestatus/' + new_uuid + '/',
            dict(state=PUBLISHED,),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Now let's test the clone and terminate endpoints for task
        # instances
        clone_response = client.post(
            '/api/executabletaskinstances/' + new_uuid + '/clone/',
            format='json',)

        new_uuid = clone_response.data['uuid']

        terminate_response = client.post(
            '/api/executabletaskinstances/' + new_uuid + '/terminate/',
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(clone_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            terminate_response.status_code,
            status.HTTP_202_ACCEPTED)

    def test_basic_http_requests_token_auth(self):
        """Make sure basic HTTP requests work using token authentication."""
        # Create a user and an authentication token
        user = User.objects.create(
            username='AzureDiamond',
            password='hunter2',)
        token = Token.objects.create(
            user=user,)

        # Start a client to make HTTP requests with
        client = APIClient()

        # Authenticate with the auth token we made
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Run tests
        self.http_requests_barrage(client)

    def test_basic_http_requests_jwt_auth(self):
        """Make sure basic HTTP requests work using JWT authentication."""
        # Create a user and an authentication token
        user = User(username='AzureDiamond')
        user.set_password('hunter2')
        user.save()

        # Start a client to make HTTP requests with
        client = APIClient()

        # Get a JWT access token and use it
        jwt_response = client.post(
            '/api/token/',
            dict(
                username='AzureDiamond',
                password='hunter2',),
            format='json',)
        access_token = jwt_response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # Run tests
        self.http_requests_barrage(client)

    def test_basic_http_requests_session_auth(self):
        """Make sure basic HTTP requests work using session authentication."""
        user = User(username='AzureDiamond')
        user.set_password('hunter2')
        user.save()

        # Start a client to make HTTP requests with
        client = APIClient()

        # Authenticate with a session
        client.login(username='AzureDiamond', password='hunter2')

        # Run tests
        self.http_requests_barrage(client)

        # Log out of the session
        client.logout()
