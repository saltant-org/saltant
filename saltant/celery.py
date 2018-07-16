"""Celery app settings."""

import os
from celery import Celery
from saltant import settings
from tasksapi.tasks import *


# Run the celery app
app = Celery('saltant')

# Set the config options specified in settings
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    broker_use_ssl=settings.BROKER_USE_SSL,
    timezone=settings.CELERY_TIMEZONE,)

# Set SSL setting if we're using SSL
try:
    app.conf.update(broker_use_ssl=settings.BROKER_USE_SSL)
except AttributeError:
    pass
