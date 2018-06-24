"""Models to represent task types and instances.

These models are validated using Django model signals in
'validators.py'.
"""

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks import tasks


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
    required_arguments = JSONField(default=list,
                                   help_text=(
                                       "A JSON array of required argument "
                                       "names"),)

    # Default arguments encoded as a dictionary. The default arguments
    # must be a subset of the required arguments, which is validated
    # when saving task types. While this validation is not strictly
    # necessary, it protects the submitter from incorrectly spelling an
    # argument name meant to be associated with a required argument
    # name.
    default_arguments = JSONField(default=dict,
                                  help_text=(
                                      "A JSON dictionary of default "
                                      "arguments, where the keys are the "
                                      "argument names and the values are "
                                      "their corresponding default values"),)

    # Path of the script to run for this task. The path is relative to
    # the task_library directory at the base directory of the Django
    # project.
    script_path = models.CharField(max_length=400,
                                   help_text=(
                                       "The path of the script to run, "
                                       "relative to the task_library "
                                       "directory"),)

    def __str__(self):
        """String representation of a task type."""
        return self.name


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
        return self.name


class TaskInstance(models.Model):
    """A running instance of a task type."""
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

    # This is set after the instance is created
    uuid = models.CharField(max_length=36,
                            editable=False,
                            null=True,
                            verbose_name="UUID",
                            help_text="The UUID for the running job",)

    # Arguments encoded as a dictionary. The arguments pass in must
    # contain all of the required arguments of the task type for which
    # there don't exist default arguments.
    arguments = JSONField(default=dict,
                          help_text=(
                              "A JSON dictionary of arguments, "
                              "where the keys are the argument "
                              "name and the values are their "
                              "corresponding values"),)

    def __str__(self):
        """String representation of a task instance."""
        return "%s (uuid %s)" % (self.task_type, self.uuid)


@receiver(post_save, sender=TaskInstance)
def start_task_instance(instance, created, **_):
    """Queue up the task instance upon creation.

    Args:
        instance: The task instance just saved.
        created: A boolean telling us if the task instance was just
            created (cf. modified).
    """
    # Only start the job if the instance was just created
    if created:
        # Use the specified queue else the default queue
        if instance.queue:
            job = tasks.run_task.apply_async(
                args=(instance.task_type.script_name,
                      instance.arguments),
                queue=instance.queue.name,)
        else:
            # Use default queue
            job = tasks.run_task.apply_async(
                args=(instance.task_type.script_path,
                      instance.arguments),)

        # Set the UUID of the instance
        instance.uuid = job.id
        instance.save()
