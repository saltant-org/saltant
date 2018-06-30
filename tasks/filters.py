"""Contains filters to go along with viewsets for the REST API."""

from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from tasks.models import TaskInstance, TaskQueue, TaskType

# Common lookups for filter fields
CHAR_FIELD_LOOKUPS = [
    'exact',
    'iexact',
    'contains',
    'icontains',
    'in',
    'startswith',
    'istartswith',
    'endswith',
    'iendswith',
    'isnull',
    'regex',
    'iregex',]
BOOLEAN_FIELD_LOOKUPS = [
    'exact',
    'iexact',
    'isnull',]
FOREIGN_KEY_FIELD_LOOKUPS = [
    'exact',
    'in',
    'isnull',]
DATE_FIELD_LOOKUPS = [
    'exact',
    'contains',
    'icontains',
    'year',
    'month',
    'day',
    'week',
    'week_day',
    'quarter',
    'hour',
    'minute',
    'regex',
    'iregex',]

class TaskInstanceFilter(filters.FilterSet):
    """A filterset to support queries for task instance attributes."""
    class Meta:
        model = TaskInstance
        fields = {
            'state': CHAR_FIELD_LOOKUPS,
            'user': FOREIGN_KEY_FIELD_LOOKUPS,
            'task_type': FOREIGN_KEY_FIELD_LOOKUPS,
            'task_queue': FOREIGN_KEY_FIELD_LOOKUPS,
            'datetime_created': DATE_FIELD_LOOKUPS,
            'datetime_finished': DATE_FIELD_LOOKUPS,}

class TaskQueueFilter(filters.FilterSet):
    """A filterset to support queries for task queue attributes."""
    class Meta:
        model = TaskQueue
        fields = {
            'name': CHAR_FIELD_LOOKUPS,
            'description': CHAR_FIELD_LOOKUPS,
            'active': BOOLEAN_FIELD_LOOKUPS,}

class TaskTypeFilter(filters.FilterSet):
    """A filterset to support queries for task type attributes."""
    class Meta:
        model = TaskType
        fields = {
            'name': CHAR_FIELD_LOOKUPS,
            'description': CHAR_FIELD_LOOKUPS,
            'script_path': CHAR_FIELD_LOOKUPS,
            'datetime_created': DATE_FIELD_LOOKUPS,}

class UserFilter(filters.FilterSet):
    """A filterset to support queries for Users."""
    class Meta:
        model = User
        fields = {
            'username': CHAR_FIELD_LOOKUPS,
            'email': CHAR_FIELD_LOOKUPS,}
