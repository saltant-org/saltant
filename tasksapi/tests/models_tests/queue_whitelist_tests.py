"""Contains tests for queue whitelists."""

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
QUEUE_PK = 1
USER_PK = 1
NON_WHITELISTED_CONTAINER_TASK_TYPE_PK = 3
NON_WHITELISTED_EXECUTABLE_TASK_TYPE_PK = 2


class TaskQueueWhitelistTests(TestCase):
    """Test task queue whitelists."""

    fixtures = ["test-fixture.yaml"]

    def setUp(self):
        """Prep common test objects."""
        self.user = User.objects.get(pk=USER_PK)
        self.executable_task_type = ExecutableTaskType.objects.get(
            pk=NON_WHITELISTED_EXECUTABLE_TASK_TYPE_PK
        )
        self.container_task_type = ContainerTaskType.objects.get(
            pk=NON_WHITELISTED_CONTAINER_TASK_TYPE_PK
        )
        self.queue = TaskQueue.objects.get(pk=QUEUE_PK)

    def test_non_whitelisted_container_task(self):
        """Test rejection of non-whtielisted container task."""
        # Ensure this doesn't go through
        with self.assertRaises(ValidationError):
            ContainerTaskInstance.objects.create(
                user=self.user,
                task_type=self.container_task_type,
                task_queue=self.queue,
            )

    def test_non_whitelisted_executable_task(self):
        """Test rejection of non-whtielisted executable task."""
        # Ensure this doesn't go through
        with self.assertRaises(ValidationError):
            ExecutableTaskInstance.objects.create(
                user=self.user,
                task_type=self.executable_task_type,
                task_queue=self.queue,
            )
