"""Forms for the frontend.

Mostly for creating task instances.
"""

from django import forms
from tasksapi.models import TaskQueue
from .widgets import JSONEditorWidget


class BaseTaskInstanceCreateForm(forms.Form):
    """Base form for creating both types of task instances."""

    task_queue = forms.ModelChoiceField(
        queryset=TaskQueue.objects.all(),
        label="Queue",
        help_text="The queue to run the task instance on.",
    )
    arguments = forms.CharField(
        widget=JSONEditorWidget(),
        help_text="Arguments required by the task type as JSON.",
    )
