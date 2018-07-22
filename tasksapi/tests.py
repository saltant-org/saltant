"""Contains tasks for the tasksapi.

This assumes a few things:
 - you're using the regular user model from django.contrib.auth
 - you've enabled (built-in) DRF token authentication
 - you've enabled DRF JWT authentication
"""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from tasksapi.constants import (
    DOCKER,
    SINGULARITY,)
from tasksapi.models import (
    TaskType,
    TaskQueue,
    TaskInstance,)


class TasksApiModelTests(TestCase):
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
