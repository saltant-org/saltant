"""Contains tests for queue permission attributes."""

from django.core.exceptions import ValidationError
from django.test import TestCase
from tasksapi.models import (
    ContainerTaskInstance,
    ContainerTaskType,
    ExecutableTaskInstance,
    ExecutableTaskType,
    TaskQueue,
    User,
)


# Put info about our fixtures data as constants here
ADMIN_PRIVATE_TASK_QUEUE_PK = 3
ADMIN_INACTIVE_TASK_QUEUE_PK = 2
EXECUTABLE_ONLY_TASK_QUEUE_PK = 4
DOCKER_CONTAINER_ONLY_TASK_QUEUE_PK = 5
SINGULARITY_CONTAINER_ONLY_TASK_QUEUE_PK = 6
EXECUTABLE_TASK_TYPE_PK = 1
DOCKER_CONTAINER_TASK_TYPE_PK = 1
SINGULARITY_CONTAINER_TASK_TYPE_PK = 2
ADMIN_USER_PK = 1
NON_ADMIN_USER_PK = 2


class TaskQueuePermissionAttributesTests(TestCase):
    """Test task queue permission attributes."""

    fixtures = ["test-fixture.yaml"]

    def setUp(self):
        """Prep common test objects."""
        # Users
        self.admin_user = User.objects.get(pk=ADMIN_USER_PK)
        self.non_admin_user = User.objects.get(pk=NON_ADMIN_USER_PK)

        # Task types
        self.executable_task_type = ExecutableTaskType.objects.get(
            pk=EXECUTABLE_TASK_TYPE_PK
        )
        self.docker_container_task_type = ContainerTaskType.objects.get(
            pk=DOCKER_CONTAINER_TASK_TYPE_PK
        )
        self.singularity_container_task_type = ContainerTaskType.objects.get(
            pk=SINGULARITY_CONTAINER_TASK_TYPE_PK
        )

        # Queues
        self.admin_private_queue = TaskQueue.objects.get(
            pk=ADMIN_PRIVATE_TASK_QUEUE_PK
        )
        self.admin_inactive_queue = TaskQueue.objects.get(
            pk=ADMIN_INACTIVE_TASK_QUEUE_PK
        )
        self.executable_only_queue = TaskQueue.objects.get(
            pk=EXECUTABLE_ONLY_TASK_QUEUE_PK
        )
        self.docker_container_only_queue = TaskQueue.objects.get(
            pk=DOCKER_CONTAINER_ONLY_TASK_QUEUE_PK
        )
        self.singularity_container_only_queue = TaskQueue.objects.get(
            pk=SINGULARITY_CONTAINER_ONLY_TASK_QUEUE_PK
        )

    def test_private_permission_attr(self):
        """Test private task queue attribute."""
        # Ensure user can post to its own private queue
        ExecutableTaskInstance.objects.create(
            user=self.admin_user,
            task_type=self.executable_task_type,
            task_queue=self.admin_private_queue,
        )
        ContainerTaskInstance.objects.create(
            user=self.admin_user,
            task_type=self.docker_container_task_type,
            task_queue=self.admin_private_queue,
        )
        ContainerTaskInstance.objects.create(
            user=self.admin_user,
            task_type=self.singularity_container_task_type,
            task_queue=self.admin_private_queue,
        )

        # Ensure user can't post to other private queue
        with self.assertRaises(ValidationError):
            ExecutableTaskInstance.objects.create(
                name="test",
                user=self.non_admin_user,
                task_type=self.executable_task_type,
                task_queue=self.admin_private_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.non_admin_user,
                task_type=self.docker_container_task_type,
                task_queue=self.admin_private_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.non_admin_user,
                task_type=self.singularity_container_task_type,
                task_queue=self.admin_private_queue,
            )

    def test_executable_permission_attr(self):
        """Test "accepts executable tasks" task queue attribute."""
        # Ensure executable tasks run fine on executable-task-only queue
        ExecutableTaskInstance.objects.create(
            user=self.admin_user,
            task_type=self.executable_task_type,
            task_queue=self.executable_only_queue,
        )

        # Ensure other tasks do not run on executable-task-only queue
        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.docker_container_task_type,
                task_queue=self.executable_only_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.singularity_container_task_type,
                task_queue=self.executable_only_queue,
            )

    def test_docker_container_permission_attr(self):
        """Test "accepts Docker container tasks" task queue attribute."""
        # Ensure Docker container tasks run fine on
        # Docker-container-tasks-only queue
        ContainerTaskInstance.objects.create(
            user=self.admin_user,
            task_type=self.docker_container_task_type,
            task_queue=self.docker_container_only_queue,
        )

        # Ensure other tasks do not run on this queue
        with self.assertRaises(ValidationError):
            ExecutableTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.executable_task_type,
                task_queue=self.docker_container_only_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.singularity_container_task_type,
                task_queue=self.docker_container_only_queue,
            )

    def test_singularity_container_permission_attr(self):
        """Test "accepts Singularity container tasks" task queue attribute."""
        # Ensure Singularity container tasks run fine on
        # Singularity-container-tasks-only queue
        ContainerTaskInstance.objects.create(
            user=self.admin_user,
            task_type=self.singularity_container_task_type,
            task_queue=self.singularity_container_only_queue,
        )

        # Ensure other tasks do not run on this queue
        with self.assertRaises(ValidationError):
            ExecutableTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.executable_task_type,
                task_queue=self.singularity_container_only_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.docker_container_task_type,
                task_queue=self.singularity_container_only_queue,
            )

    def test_active_permission_attr(self):
        """Test active task queue attribute."""
        # Ensure user can't post to its own inactive queue
        with self.assertRaises(ValidationError):
            ExecutableTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.executable_task_type,
                task_queue=self.admin_inactive_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.docker_container_task_type,
                task_queue=self.admin_inactive_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.admin_user,
                task_type=self.singularity_container_task_type,
                task_queue=self.admin_inactive_queue,
            )

        # Ensure user can't post to other inactive queue
        with self.assertRaises(ValidationError):
            ExecutableTaskInstance.objects.create(
                user=self.non_admin_user,
                task_type=self.executable_task_type,
                task_queue=self.admin_inactive_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.non_admin_user,
                task_type=self.docker_container_task_type,
                task_queue=self.admin_inactive_queue,
            )

        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.non_admin_user,
                task_type=self.singularity_container_task_type,
                task_queue=self.admin_inactive_queue,
            )
