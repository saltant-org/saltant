"""Contains model tests for the tasksapi."""

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tasksapi.constants import DOCKER
from tasksapi.models import (
    ContainerTaskInstance,
    ContainerTaskType,
    TaskQueue,)


class TasksApiModelTests(TransactionTestCase):
    """Test that we can instantiate models correctly."""
    def test_container_task_model_creation(self):
        """Make sure basic model instantiation doesn't fail."""
        # Create a user
        user = User.objects.create(
            username='AzureDiamond',
            password='hunter2',)

        # Create a container task type
        tasktype = ContainerTaskType.objects.create(
            name='my-task-type',
            description="Fantastic task type",
            user=user,
            container_image='mwiens91/hello-world',
            container_type=DOCKER,
            command_to_run='/app/hello_world.py',
            logs_path='/logs/',
            results_path='/results/',
            environment_variables=['HOME'],
            required_arguments=['name'],
            required_arguments_default_values={'name': 'AzureDiamond'},)

        # Create a task queue
        taskqueue = TaskQueue.objects.create(
            name='my-task-queue',
            description="Fantastic task queue",
            user=user,
            private=False,
            active=True,)

        # Create a task instance of the task type we made and assign it
        # to the task queue we made
        taskinstance = ContainerTaskInstance.objects.create(
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
