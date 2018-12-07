"""Forms for the frontend."""

from django import forms
from tasksapi.models import ContainerTaskType, ExecutableTaskType, TaskQueue
from .widgets import JSONEditorWidget


class BaseTaskInstanceCreateForm(forms.Form):
    """Base form for creating both types of task instances."""

    name = forms.CharField(
        required=False, help_text="An optional name for the task instance"
    )
    task_queue = forms.ModelChoiceField(
        queryset=TaskQueue.objects.all(),
        label="Queue",
        help_text="The queue to run the task instance on.",
    )
    arguments = forms.CharField(
        widget=JSONEditorWidget(),
        help_text="Arguments required by the task type as JSON.",
    )


# When creating a task instance, one must first specify a task type to
# base it off of. (Technically they could do so in the same form, but
# that's more work given the initial data setting features.)
class ContainerTaskTypeSelectForm(forms.Form):
    """Form for selecting a container task type."""

    task_type = forms.ModelChoiceField(
        queryset=ContainerTaskType.objects.all()
    )


class ExecutableTaskTypeSelectForm(forms.Form):
    """Form for selecting an executable task type."""

    task_type = forms.ModelChoiceField(
        queryset=ExecutableTaskType.objects.all()
    )
