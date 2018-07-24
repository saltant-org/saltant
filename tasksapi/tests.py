"""Contains tasks for the tasksapi.

This assumes a few things:
 - you're using the regular user model from django.contrib.auth
 - you've enabled (built-in) DRF token authentication
 - you've enabled DRF JWT authentication
"""

import pathlib
import os
import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APIClient,
    APITransactionTestCase,)
from tasksapi.constants import (
    PUBLISHED,
    DOCKER,)
from tasksapi.models import (
    TaskType,
    TaskQueue,
    TaskInstance,)
from tasksapi.tasks import (
    run_docker_container_executable,
    run_singularity_container_executable,)


class TasksApiModelTests(TransactionTestCase):
    """Test that we can instantiate models correctly."""
    def test_model_creation(self):
        """Make sure basic model instantiation doesn't fail."""
        # Create a user
        user = User.objects.create(
            username='AzureDiamond',
            password='hunter2',)

        # Create a task type
        tasktype = TaskType.objects.create(
            name='my-task-type',
            description="Fantastic task type",
            user=user,
            container_image='mwiens91/hello-world',
            container_type=DOCKER,
            script_path='apps/hello_world.py',
            logs_path='/logs/',
            environment_variables=['HOME'],
            required_arguments=['name'],
            required_arguments_default_values={'name': 'AzureDiamond'},
            directories_to_bind={},)

        # Create a task queue
        taskqueue = TaskQueue.objects.create(
            name='my-task-queue',
            description="Fantastic task queue",
            user=user,
            private=False,
            active=True,)

        # Create a task instance of the task type we made and assign it
        # to the task queue we made
        taskinstance = TaskInstance.objects.create(
            name='my-task-instance',
            user=user,
            task_type=tasktype,
            task_queue=taskqueue,
            arguments={'name': 'Daniel'},)

        # Now delete everything
        taskinstance.delete()
        taskqueue.delete()
        tasktype.delete()
        user.delete()


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
        # POST, GET, and PUT a task type
        post_response = client.post(
            '/api/tasktypes/',
            dict(
                name='my-task-type',
                description="Fantastic task type",
                user=1,
                container_image='mwiens91/hello-world',
                container_type=DOCKER,
                script_path='apps/hello_world.py',
                logs_path='/logs/',
                environment_variables=['HOME'],
                required_arguments=['name'],
                required_arguments_default_values={'name': 'AzureDiamond'},
                directories_to_bind={},),
            format='json',)
        get_response_1 = client.get(
            '/api/tasktypes/',
            format='json',)
        get_response_2 = client.get(
            '/api/tasktypes/1/',
            format='json',)
        put_response = client.put(
            '/api/tasktypes/1/',
            dict(
                name='my-task-type',
                description="Fantastic task type 2",
                user=1,
                container_image='mwiens91/hello-world',
                container_type=DOCKER,
                script_path='apps/hello_world.py',
                logs_path='/logs/',
                environment_variables=['HOME'],
                required_arguments=['name'],
                required_arguments_default_values={'name': 'AzureDiamond'},
                directories_to_bind={},),
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
                user=1,
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
                user=1,
                private=False,
                active=True,),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PATCH a task instance, passing in explicitly
        # the task type
        post_response = client.post(
            '/api/taskinstances/',
            dict(
                name='my-task-instance',
                user=1,
                task_type=1,
                task_queue=1,
                arguments={'name': 'Daniel'},),
            format='json',)

        # Get the UUID of the task instance we just made
        new_uuid = post_response.data['uuid']

        # Continue with the requests
        get_response_1 = client.get(
            '/api/taskinstances/',
            format='json',)
        get_response_2 = client.get(
            '/api/taskinstances/' + new_uuid + '/',
            format='json',)
        patch_response = client.patch(
            '/api/taskinstances/' + new_uuid + '/',
            dict(state=PUBLISHED,),
            format='json',)

        # Make sure we get the right statuses in response to our
        # requests
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # POST, GET, and PATCH a task instance, passing in the task type
        # through the URL
        post_response = client.post(
            '/api/tasktypes/1/instances/',
            dict(
                name='my-task-instance',
                user=1,
                task_queue=1,
                arguments={'name': 'Daniel'},),
            format='json',)

        # Get the UUID of the task instance we just made
        new_uuid = post_response.data['uuid']

        # Continue with the requests
        get_response_1 = client.get(
            '/api/tasktypes/1/instances/',
            format='json',)
        get_response_2 = client.get(
            '/api/tasktypes/1/instances/' + new_uuid + '/',
            format='json',)
        patch_response = client.patch(
            '/api/tasktypes/1/instances/' + new_uuid + '/',
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
            '/api/taskinstances/' + new_uuid + '/clone/',
            format='json',)

        new_uuid = clone_response.data['uuid']

        terminate_response = client.post(
            '/api/taskinstances/' + new_uuid + '/terminate/',
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


class TasksApiContainerTests(TestCase):
    """Test tasks functionality.

    Using the Docker container defined here:
    https://github.com/mwiens91/saltant-test-docker-container.
    """
    @classmethod
    def setUpTestData(cls):
        """Create some temporary directories to store job results."""
        # Generate the base path for this test
        cls.base_dir_name = os.path.join(
            settings.BASE_DIR,
            'temp-test-' + str(uuid.uuid4()),)

        # Make the logs and singularity images directories
        cls.logs_path = os.path.join(
            cls.base_dir_name,
            'logs/',)
        cls.singularity_path = os.path.join(
            cls.base_dir_name,
            'images/',)
        pathlib.Path(cls.logs_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(cls.singularity_path).mkdir(parents=True, exist_ok=True)

        # Overload our environment variables to use our generated temp
        # storage directories
        os.environ['WORKER_LOGS_DIRECTORY'] = cls.logs_path
        os.environ['WORKER_SINGULARITY_IMAGES_DIRECTORY'] = (
            cls.singularity_path)

    def tearDown(self):
        """Clean up directories made in setUpTestData."""
        pass
        # TODO: this command fails because the files that the Docker
        # container are owned by 'root'. Looked into this a bit, but
        # couldn't find a clean solution, so right now there's no
        # automatic cleanup :(
        #shutil.rmtree(self.base_dir_name)

    def test_docker(self):
        """Make sure Docker jobs work properly."""
        run_docker_container_executable(
            uuid='test-docker-uuid',
            container_image='mwiens91/hello-world',
            executable_path='/app/hello_world.py',
            logs_path='/logs/',
            directories_to_bind={'/tmp/': '/bindme/'},
            env_vars_list=['SHELL',],
            args_dict={'name': 'AzureDiamond'},)

    def test_singularity(self):
        """Make sure Singularity jobs work properly."""
        run_singularity_container_executable(
            uuid='test-singularity-uuid',
            container_image='docker://mwiens91/hello-world',
            executable_path='/app/hello_world.py',
            logs_path='/logs/',
            directories_to_bind={'/tmp/': '/bindme/'},
            env_vars_list=['SHELL',],
            args_dict={'name': 'AzureDiamond'},)
