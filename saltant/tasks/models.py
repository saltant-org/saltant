"""Models to represent task types and instances.

These models are validated using Django model signals in
'validators.py'.
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class TaskType(models.Model):
    """A type of task to create instances with."""
    name = models.CharField(max_length=50,
                            unique=True,
                            help_text="The name of the task",)
    description = models.TextField(blank=True,
                                   null=True,
                                   help_text="A description of the task",)

    # The datetime the task type was created. This will be automatically
    # set upon creation of a task type and is *not* editable. See
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    # for more details.
    datetime_created = models.DateTimeField(auto_now_add=True)

    # Required arguments
    required_arguments = JSONField(blank=True,
                                   null=True,
                                   help_text=(
                                       "A list of required argument names"),)

    # Default arguments encoded as a dictionary. The default arguments
    # must be a subset of the required arguments, which is validated
    # when saving task types. While this validation is not strictly
    # necessary, it protects the submitter from incorrectly spelling an
    # argument name meant to be associated with a required argument
    # name.
    default_arguments = JSONField(blank=True,
                                  null=True,
                                  help_text=(
                                      "A dictionary of default arguments, "
                                      "where the keys are the argument "
                                      "name and the values are their "
                                      "corresponding default values"),)

    # Path of the script to run for this task. The path is relative to
    # the task_scripts directory at the base directory of the Django
    # project.
    script_path = models.CharField(max_length=400,
                                   help_text=(
                                       "The path of the script to run, "
                                       "relative to the task_scripts "
                                       "directory"),)

    def __str__(self):
        """String representation of a task type."""
        return name


class TaskScheduler(models.Model):
    """Spawns reoccuring instances of a task type."""
    pass


class TaskQueue(models.Model):
    """The Celery queue on which task instances run."""
    name = models.CharField(max_length=50,
                            unique=True,
                            help_text="The name of the Celery queue",)
    description = models.TextField(blank=True,
                                   null=True,
                                   help_text="A description of the queue",)
    active = models.BooleanField(default=True,
                                 help_text=(
                                     "A boolean showing the status of the "
                                     "queue. As of now, this needs to be "
                                     "toggled manually."),)

    def __str__(self):
        """String representation of a queue."""
        return name


class TaskInstance(models.Model):
    """A running instance of a task type."""
    name = models.CharField(max_length=50,
                            help_text="The name of the instance",)
    task_type = models.ForeignKey(TaskType,
                                  null=True,
                                  on_delete=models.SET_NULL,
                                  help_text=(
                                      "The task type for which this "
                                      "is an instance"),)
    author = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL,
                               help_text="The author of this instance",)
    queue = models.ForeignKey(TaskQueue,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              help_text=(
                                  "The queue this instance runs on. "
                                  "If left blank, then the default "
                                  "queue is used."),)
    datetime_created = models.DateTimeField(auto_now_add=True)

    # Arguments encoded as a dictionary. The arguments pass in must
    # contain all of the required arguments of the task type for which
    # there don't exist default arguments.
    arguments = JSONField(blank=True,
                          null=True,
                          help_text=(
                              "A dictionary of arguments, "
                              "where the keys are the argument "
                              "name and the values are their "
                              "corresponding values"),)

    def __str__(self):
        """String representation of a task instance."""
        return "%s (%s)" % (name, task_type)
