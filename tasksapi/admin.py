"""Register models with the admin site."""

from django.contrib import admin
from tasksapi.models import (
    TaskInstance,
    TaskQueue,
    TaskType,)

@admin.register(TaskInstance)
class TaskInstanceAdmin(admin.ModelAdmin):
    """Interface modifiers for task instances on the admin page."""
    list_display = ('uuid',
                    'task_type',
                    'task_queue',
                    'state',
                    'datetime_created',
                    'datetime_finished',
                    'user',)

@admin.register(TaskQueue)
class TaskQueueAdmin(admin.ModelAdmin):
    """Interface modifiers for task queues on the admin page."""
    list_display = ('name',
                    'user',
                    'private',
                    'active',)

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    """Interface modifiers for task types on the admin page."""
    list_display = ('name',
                    'user',
                    'container_image',
                    'container_type',
                    'script_path',
                    'datetime_created',)
