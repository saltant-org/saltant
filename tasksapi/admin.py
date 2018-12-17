"""Register models with the admin site."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tasksapi.models import (
    ContainerTaskInstance,
    ContainerTaskType,
    ExecutableTaskInstance,
    ExecutableTaskType,
    TaskQueue,
    TaskWhitelist,
    User,
)


@admin.register(ContainerTaskInstance)
class ContainerTaskInstanceAdmin(admin.ModelAdmin):
    """Interface modifiers for container task instances on the admin page."""

    list_display = (
        "uuid",
        "task_type",
        "task_queue",
        "state",
        "name",
        "datetime_created",
        "datetime_finished",
        "user",
    )


@admin.register(ContainerTaskType)
class ContainerTaskTypeAdmin(admin.ModelAdmin):
    """Interface modifiers for container task types on the admin page."""

    list_display = (
        "name",
        "user",
        "container_image",
        "container_type",
        "command_to_run",
        "datetime_created",
        "user",
    )


@admin.register(ExecutableTaskInstance)
class ExecutableTaskInstanceAdmin(admin.ModelAdmin):
    """Interface modifiers for container task instances on the admin page."""

    list_display = (
        "uuid",
        "task_type",
        "task_queue",
        "state",
        "name",
        "datetime_created",
        "datetime_finished",
        "user",
    )


@admin.register(ExecutableTaskType)
class ExecutableTaskTypeAdmin(admin.ModelAdmin):
    """Interface modifiers for container task types on the admin page."""

    list_display = (
        "name",
        "user",
        "command_to_run",
        "datetime_created",
        "user",
    )


@admin.register(TaskQueue)
class TaskQueueAdmin(admin.ModelAdmin):
    """Interface modifiers for task queues on the admin page."""

    list_display = ("name", "user", "private", "active")


@admin.register(TaskWhitelist)
class TaskWhitelistAdmin(admin.ModelAdmin):
    """Interface modifiers for task queues on the admin page."""

    list_display = ("name",)


# Register custom user
admin.site.register(User, UserAdmin)
