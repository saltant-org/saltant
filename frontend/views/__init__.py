"""Contains views for the frontend."""

# Make stuff in this package visible
from .misc import Home, About, TaskTypeRedirect, TaskInstanceRedirect
from .queues import (
    QueueList,
    QueueCreate,
    QueueDetail,
    QueueUpdate,
    QueueDelete,
)
from .taskinstances import (
    ContainerTaskInstanceList,
    ContainerTaskInstanceDetail,
    ExecutableTaskInstanceDetail,
    ExecutableTaskInstanceList,
)
from .tasktypes import ContainerTaskTypeList, ExecutableTaskTypeList
