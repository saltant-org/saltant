"""Contains tasks to register with Celery."""

import os
from celery import shared_task
from celery.signals import (
    after_task_publish,
    task_prerun,
    task_success,
    task_failure,
    task_revoked,)
import requests
from tasks.constants import (
    CREATED,
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,)


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


@after_task_publish.connect
def task_sent_handler(**kwargs):
    """Update the state of the task instance.

    Note that this function is processed by the process sending the
    task. Also note that the kwarg dictionaries given to the various
    handlers in general do not contain the same information, and if they
    do, then in general they will not share the same schema.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['ADMIN_AUTH_TOKEN'],
               job_uuid=str(kwargs['headers']['id']),
               state=PUBLISHED,)


@task_prerun.connect
def task_prerun_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['ADMIN_AUTH_TOKEN'],
               job_uuid=str(kwargs['task_id']),
               state=RUNNING,)


@task_success.connect
def task_success_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['ADMIN_AUTH_TOKEN'],
               job_uuid=kwargs['sender'].request.id,
               state=SUCCESSFUL,)


@task_failure.connect
def task_failure_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['ADMIN_AUTH_TOKEN'],
               job_uuid=kwargs['task_id'],
               state=FAILED,)


@task_revoked.connect
def task_revoked_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['ADMIN_AUTH_TOKEN'],
                job_uuid=kwargs['request'].task_id,
                state=TERMINATED,)
