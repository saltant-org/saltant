"""Contains tasks to register with Celery."""

from celery import shared_task
from celery.signals import (
    after_task_publish,
    task_prerun,
    task_success,
    task_failure,)
from tasks.constants import (
    CREATED,
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    REVOKED,)


@shared_task
def run_task(script_path, jsonargs):
    """Run the script at script_path with jsonargs."""
    return "Hello world!"

#
# The following is a work in progress. Essentially what should happen is
# that Celery signals should be intercepted at various points to
# indicate the state of a job. The state of the job in the Saltant DB
# should be updated to reflect this with an API PUT call; note that all
# the signals (I think?) have access to the job's UUID
#

@after_task_publish.connect
def task_sent_handler(root_id, **_):
    """Update the state of the task instance.

    Note that this function is processed by the process sending the
    task.

    Arg:
        root_id: A string containing the UUID of the task.
    """
    print("IN AFTER TASK PUBLISH")

@task_prerun.connect
def task_prerun_handler(**kwargs):
    """Update the state of the task instance."""
    print("IN TASK PRERUN")
    print(kwargs)

@task_success.connect
def task_success_handler(**kwargs):
    print("IN TASK SUCCESS")
    print(kwargs)

@task_failure.connect
def task_failure_handler(**kwargs):
    print("IN TASK FAILURE")
    print(kwargs)
