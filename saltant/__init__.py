"""Make sure shared_tasks use the celery app."""

from saltant.celery import app as celery_app

__all__ = ('celery_app',)
