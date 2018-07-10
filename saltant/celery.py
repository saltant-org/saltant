"""Celery app settings."""

import os
from celery import Celery
from saltant import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saltant.settings')

app = Celery('saltant')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# For some reason the BROKER_USE_SSL isn't being loaded properly by the
# above command
try:
    app.conf.update(broker_use_ssl=settings.BROKER_USE_SSL)
except AttributeError:
    pass

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
