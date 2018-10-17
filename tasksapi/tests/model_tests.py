"""Contains model tests for the tasksapi."""

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tasksapi.constants import DOCKER
from tasksapi.models import (
    ContainerTaskInstance,
    ContainerTaskType,
    ExecutableTaskInstance,
    ExecutableTaskType,
    TaskQueue,
)


class TasksApiModelTests(TransactionTestCase):
    """Test that we can instantiate models correctly."""

    def test_container_task_model_creation(self):
        """Make sure basic model instantiation doesn't fail."""
        # Create a user
        user = User.objects.create(username="AzureDiamond", password="hunter2")

        # Create a container task type
        containertasktype = ContainerTaskType.objects.create(
            name="my-container-task-type",
            description="Fantastic task type",
            user=user,
            container_image="mwiens91/hello-world",
            container_type=DOCKER,
            command_to_run="/app/hello_world.py",
            logs_path="/logs/",
            results_path="/results/",
            environment_variables=["HOME"],
            required_arguments=["name"],
            required_arguments_default_values={"name": "AzureDiamond"},
        )

        # Create an executable task type
        executabletasktype = ExecutableTaskType.objects.create(
            name="my-executable-task-type",
            description="Fantastic task type",
            user=user,
            command_to_run="true",
        )

        # Create a task queue
        taskqueue = TaskQueue.objects.create(
            name="my-task-queue",
            description="Fantastic task queue",
            user=user,
            private=False,
            active=True,
        )

        # Create a task instance of the container task type we made and
        # assign it to the task queue we made
        containertaskinstance = ContainerTaskInstance.objects.create(
            name="my-task-instance",
            user=user,
            task_type=containertasktype,
            task_queue=taskqueue,
            arguments={"name": "Daniel"},
        )

        # Create a task instance of the executable task type we made and
        # assign it to the task queue we made
        executabletaskinstance = ExecutableTaskInstance.objects.create(
            name="my-task-instance",
            user=user,
            task_type=executabletasktype,
            task_queue=taskqueue,
        )

        # Now delete everything
        containertaskinstance.delete()
        executabletaskinstance.delete()
        taskqueue.delete()
        containertasktype.delete()
        executabletasktype.delete()
        user.delete()
