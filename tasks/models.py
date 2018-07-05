"""Models to represent task types and instances."""

import json
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from tasks.constants import (
    CREATED,
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
    DOCKER,
    SINGULARITY,)
from tasks.tasks import run_task
from tasks.validators import (
    task_instance_args_are_valid,
    task_type_args_are_valid,)


# RegexValidator for validating a TaskType name.
sane_name_validator = RegexValidator(
    regex=r'^[\w@+-]+$',
    message=" @/+/-/_ only",)


class TaskType(models.Model):
    """A type of task to create instances with."""
    # Choices for the container type field
    CONTAINER_CHOICES = (
        (DOCKER, 'Docker'),
        (SINGULARITY, 'Singularity'),)

    name = models.CharField(max_length=50,
                            validators=[sane_name_validator,],
                            help_text="The name of the task",)
    description = models.TextField(blank=True,
                                   help_text="A description of the task",)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             help_text="The author of this task",)

    # The datetime the task type was created. This will be automatically
    # set upon creation of a task type and is *not* editable. See
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    # for more details.
    datetime_created = models.DateTimeField(auto_now_add=True)

    # Container info
    container_image = models.CharField(max_length=200,
                                       help_text=(
                                           "The container name and tag. "
                                           "E.g., \"ubuntu:14.04\"."),)
    container_type = models.CharField(max_length=11,
                                      choices=CONTAINER_CHOICES,
                                      help_text=(
                                          "The type of container "
                                          "provided"),)
    script_path = models.CharField(max_length=400,
                                   help_text=(
                                       "The path of the script to run, "
                                       "inside of the container image. "
                                       "*Must* be executable!"),)

    # Required arguments
    required_arguments = JSONField(blank=True,
                                   default=list,
                                   help_text=(
                                       "A JSON array of required argument "
                                       "names"),)

    # Default arguments encoded as a dictionary. The default arguments
    # must be a subset of the required arguments, which is validated
    # when saving task types. While this validation is not strictly
    # necessary, it protects the submitter from incorrectly spelling an
    # argument name meant to be associated with a required argument
    # name.
    default_arguments = JSONField(blank=True,
                                  default=dict,
                                  help_text=(
                                      "A JSON dictionary of default "
                                      "arguments, where the keys are the "
                                      "argument names and the values are "
                                      "their corresponding default values"),)

    class Meta:
        unique_together = (('name', 'user'),)

    def __str__(self):
        """String representation of a task type."""
        return self.name

    def save(self, *args, **kwargs):
        # Call clean
        self.clean()

        # Call the parent save method
        super().save(*args, **kwargs)

    def clean(self):
        """Validate a task type's required arguments."""
        # If JSON was passed in as a string, try to interpret it as JSON
        if isinstance(self.required_arguments, str):
            try:
                self.required_arguments = json.loads(self.required_arguments)
            except json.JSONDecodeError:
                raise ValidationError("'%s' is not valid JSON!"
                                      % self.required_arguments)

        if isinstance(self.default_arguments, str):
            try:
                self.default_arguments = json.loads(self.default_arguments)
            except json.JSONDecodeError:
                raise ValidationError("'%s' is not valid JSON!"
                                      % self.default_arguments)

        # Make sure arguments are valid
        is_valid, reason = task_type_args_are_valid(self)

        # Arguments are not valid!
        if not is_valid:
            raise ValidationError(reason)


class TaskScheduler(models.Model):
    """Spawns reoccuring instances of a task type."""
    pass


class TaskQueue(models.Model):
    """The Celery queue on which task instances run."""
    name = models.CharField(max_length=50,
                            unique=True,
                            validators=[sane_name_validator,],
                            help_text="The name of the Celery queue",)
    description = models.TextField(blank=True,
                                   help_text="A description of the queue",)
    active = models.BooleanField(blank=True,
                                 default=True,
                                 help_text=(
                                     "A boolean showing the status of the "
                                     "queue. As of now, this needs to be "
                                     "toggled manually."),)

    def __str__(self):
        """String representation of a queue."""
        return self.name


class TaskInstance(models.Model):
    """A running instance of a task type."""
    # Choices for the state field (following recommended convention at
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#choices.
    # The states are based off of signals provided by Celery (which in
    # fact set the state field):
    # http://docs.celeryproject.org/en/master/userguide/signals.html.
    STATE_CHOICES = (
        (CREATED, 'created'),
        (PUBLISHED, 'published'),
        (RUNNING, 'running'),
        (SUCCESSFUL, 'successful'),
        (FAILED, 'failed'),
        (TERMINATED, 'terminated'),)

    uuid = models.UUIDField(primary_key=True,
                            default=uuid4,
                            editable=False,
                            verbose_name="UUID",
                            help_text="The UUID for the running job",)
    state = models.CharField(max_length=10,
                             choices=STATE_CHOICES,
                             default=CREATED,)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             help_text="The author of this instance",)
    task_type = models.ForeignKey(TaskType,
                                  on_delete=models.PROTECT,
                                  help_text=(
                                      "The task type for which this "
                                      "is an instance"),)
    task_queue = models.ForeignKey(TaskQueue,
                                   on_delete=models.PROTECT,
                                   help_text=(
                                       "The queue this instance runs on. "
                                       "If left blank, then the default "
                                       "queue is used."),)
    datetime_created = models.DateTimeField(auto_now_add=True,
                                            help_text=(
                                                "When the job was created"),)
    datetime_finished = models.DateTimeField(null=True,
                                             editable=False,
                                             help_text=(
                                                 "When the job finished."),)

    # Arguments encoded as a dictionary. The arguments pass in must
    # contain all of the required arguments of the task type for which
    # there don't exist default arguments.
    arguments = JSONField(blank=True,
                          default=dict,
                          help_text=(
                              "A JSON dictionary of arguments, "
                              "where the keys are the argument "
                              "name and the values are their "
                              "corresponding values"),)

    class Meta:
        """Model metadata."""
        ordering = ['-datetime_created']

    def __str__(self):
        """String representation of a task instance."""
        return "%s (uuid %s)" % (self.task_type, self.uuid)

    def save(self, *args, **kwargs):
        """Perform additonal validation."""
        # Call clean
        self.clean(fill_in_missing_args=True)

        # Call the parent save method
        super().save(*args, **kwargs)

    def clean(self, fill_in_missing_args=False):
        """Validate a instance's arguments."""
        # If JSON was passed in as a string, try to interpret it as JSON
        if isinstance(self.arguments, str):
            try:
                self.arguments = json.loads(self.arguments)
            except json.JSONDecodeError:
                raise ValidationError("%s is not valid JSON!"
                                      % self.arguments)

        # Make sure arguments are valid
        is_valid, reason = task_instance_args_are_valid(
            instance=self,
            fill_missing_args=fill_in_missing_args)

        # Arguments are not valid!
        if not is_valid:
            raise ValidationError(reason)


@receiver(pre_save, sender=TaskInstance)
def task_instance_pre_save_handler(instance, **_):
    """Adds additional behavior before saving a task instance.

    If the state is about to be changed to a finished change, update the
    datetime finished field.

    Args:
        instance: The task instance about to be saved.
    """
    if instance.state in (SUCCESSFUL, FAILED):
        instance.datetime_finished = timezone.now()


@receiver(post_save, sender=TaskInstance)
def task_instance_post_save_handler(instance, created, **_):
    """Adds additional behavior after saving a task instance.

    Right now this just queues up the task instance upon creation.

    Args:
        instance: The task instance just saved.
        created: A boolean telling us if the task instance was just
            created (cf. modified).
    """
    # Only start the job if the instance was just created
    if created:
        # Use the specified queue else the default queue
        kwargs = {
            'uuid': instance.uuid,
            'container_image': instance.task_type.container_image,
            'container_type': instance.task_type.container_type,
            'script_path': instance.task_type.script_path,
            'args_dict': instance.arguments,}

        run_task.apply_async(
            kwargs=kwargs,
            queue=instance.task_queue.name,
            task_id=instance.uuid,)
