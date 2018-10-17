"""Things here get run first.

This initializes the Celery app, and makes sure that environment
variables are loaded for it.
"""

from __future__ import absolute_import  # for Python 2.x workers
import os
import dotenv

# Load environment variables
dotenv.read_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
)

# Initialize Celery (see
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
from saltant.celery import app as celery_app

__all__ = ("celery_app",)
