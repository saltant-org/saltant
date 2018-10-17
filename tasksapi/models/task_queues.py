"""Model to represent task queues."""

from django.contrib.auth.models import User
from django.db import models
from .utils import sane_name_validator


class TaskQueue(models.Model):
    """The Celery queue on which task instances run."""
    name = models.CharField(max_length=50,
                            unique=True,
                            validators=[sane_name_validator,],
                            help_text="The name of the Celery queue.",)
    description = models.TextField(blank=True,
                                   help_text="A description of the queue.",)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             help_text="The creator of the queue.",)
    private = models.BooleanField(blank=True,
                                  default=False,
                                  help_text=(
                                      "A boolean specifying whether "
                                      "other users besides the queue creator "
                                      "can use the queue. Defaults to False."),)
    active = models.BooleanField(blank=True,
                                 default=True,
                                 help_text=(
                                     "A boolean showing the status of the "
                                     "queue. As of now, this needs to be "
                                     "toggled manually. Defaults to True."),)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String representation of a queue."""
        return self.name
