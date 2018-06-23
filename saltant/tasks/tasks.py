"""Contains tasks to register with Celery."""

from celery import shared_task

# Misc tasks
@shared_task
def hello_world(name):
    return "Hello world, %s!" % name
