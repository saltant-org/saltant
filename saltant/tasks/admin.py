"""Register models with the admin site."""

from django.contrib import admin
from tasks.models import TaskInstance, TaskType

@admin.register(TaskInstance)
class TaskInstanceAdmin(admin.ModelAdmin):
    """Interface modifiers for task instances on the admin page."""
    list_display = ('name', 'task_type', 'author',)

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    """Interface modifiers for task types on the admin page."""
    list_display = ('name', 'script_path',)
