"""Contains tasks to register with Celery."""

import os
from celery import shared_task
from celery.signals import (
    after_task_publish,
    task_prerun,
    task_success,
    task_failure,)
import requests
from tasks.constants import (
    CREATED,
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    REVOKED,)


@shared_task
def run_task(script_path, jsonargs):
    """Run the script at script_path with jsonargs.

    This is the main function used to launch all tasks instance jobs.
    """
    # Currently just print Hello World until I develop proper
    # functionality here
    return "Hello world!"


def update_job(api_token, job_uuid, state):
    """Update the status of the job.

    Args:
        api_token: A string containing a valid token for the API.
        job_uuid: A string containing the UUID for the task instance to
            update.
        state: A string which must be one of the state constants.
    Returns:
        A requests.Response object containing the server's response to
            the HTTP request.
    """
    # Form the API endpoint URL
    base_url = os.environ['DJANGO_BASE_URL']
    endpoint_url_pieces = (
        base_url,
        r'/api/taskinstances/',
        job_uuid,)
    endpoint_url = '/'.join(s.strip('/') for s in endpoint_url_pieces)

    # Make the HTTP request
    return requests.patch(
        endpoint_url,
        data={'state': state},
        headers={'Authorization': 'Token {}'.format(api_token)},)


#
# The following is a work in progress. Essentially what should happen is
# that Celery signals should be intercepted at various points to
# indicate the state of a job. The state of the job in the Saltant DB
# should be updated to reflect this with an API PATCH call; note that
# all the signals (I think?) have access to the job's UUID
#

@after_task_publish.connect
def task_sent_handler(**kwargs):
    """Update the state of the task instance.

    Note that this function is processed by the process sending the
    task.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['ADMIN_AUTH_TOKEN'],
               job_uuid=str(kwargs['headers']['id']),
               state=PUBLISHED,)

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
