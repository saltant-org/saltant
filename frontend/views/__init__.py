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
    ContainerTaskInstanceRename,
    ContainerTaskInstanceStateUpdate,
    ContainerTaskInstanceTerminate,
    ContainerTaskInstanceDelete,
    ExecutableTaskInstanceList,
    ExecutableTaskInstanceDetail,
    ExecutableTaskInstanceRename,
    ExecutableTaskInstanceStateUpdate,
    ExecutableTaskInstanceTerminate,
    ExecutableTaskInstanceDelete,
)
from .taskinstances_create import (
    ContainerTaskInstanceClone,
    ContainerTaskInstanceCreate,
    ExecutableTaskInstanceClone,
    ExecutableTaskInstanceCreate,
)
from .tasktypes import (
    ContainerTaskTypeList,
    ContainerTaskTypeDetail,
    ExecutableTaskTypeList,
    ExecutableTaskTypeDetail,
)
