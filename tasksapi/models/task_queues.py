"""Model to represent task queues."""

from django.db import models
from .users import User
from .utils import sane_name_validator


class TaskQueue(models.Model):
    """The Celery queue on which task instances run.

    With some extra annotations and *light* security measures.
    ("*light*" meaning that you can probably get around them pretty
    easily if you decide to hit the messaging queue (e.g., RabbitMQ)
    directly.)
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[sane_name_validator],
        help_text="The name of the Celery queue.",
    )
    description = models.TextField(
        blank=True, help_text="A description of the queue."
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The creator of the queue."
    )
    private = models.BooleanField(
        blank=True,
        default=False,
        help_text=(
            "A boolean specifying whether "
            "other users besides the queue creator "
            "can use the queue. Defaults to False."
        ),
    )
    runs_executable_tasks = models.BooleanField(
        blank=True,
        default=True,
        help_text=(
            "A boolean specifying whether the queue runs executable tasks. "
            "Defaults to True."
        ),
    )
    runs_docker_container_tasks = models.BooleanField(
        blank=True,
        default=True,
        verbose_name="runs Docker container tasks",
        help_text=(
            "A boolean specifying whether the queue runs container "
            "tasks that run in Docker containers. Defaults to True."
        ),
    )
    runs_singularity_container_tasks = models.BooleanField(
        blank=True,
        default=True,
        verbose_name="runs Singularity container tasks",
        help_text=(
            "A boolean specifying whether the queue runs container "
            "tasks that run in Singularity containers. Defaults to True."
        ),
    )
    active = models.BooleanField(
        blank=True,
        default=True,
        help_text=(
            "A boolean showing the status of the "
            "queue. As of now, this needs to be "
            "toggled manually. Defaults to True."
        ),
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        """String representation of a queue."""
        return self.name
