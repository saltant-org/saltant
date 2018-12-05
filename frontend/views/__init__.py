"""Contains views for the frontend."""

# Make stuff in this package visible
from .accounts import UserUpdate
from .errors import (
    BadRequest400,
    PermissionDenied403,
    PageNotFound404,
    ServerError500,
)
from .misc import (
    Home,
    About,
    TaskTypeRedirect,
    TaskInstanceRedirect,
    ContainerTaskInstanceCreateTaskTypeMenu,
    ExecutableTaskInstanceCreateTaskTypeMenu,
)
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
    ContainerTaskTypeCreate,
    ContainerTaskTypeDetail,
    ContainerTaskTypeUpdate,
    ContainerTaskTypeDelete,
    ExecutableTaskTypeList,
    ExecutableTaskTypeCreate,
    ExecutableTaskTypeDetail,
    ExecutableTaskTypeUpdate,
    ExecutableTaskTypeDelete,
)
