"""Contains tasks to register with Celery."""

from celery import shared_task

# Misc tasks
@shared_task
def run_task(script_path, jsonargs):
    return "Hello world!"
