"""Contains the base task and signal handlers to register with Celery."""

import os
from celery import shared_task
from celery.signals import (
    after_task_publish,
    task_prerun,
    task_success,
    task_failure,
    task_revoked,)
import requests
from tasksapi.constants import (
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
    CONTAINER_TASK,
    EXECUTABLE_TASK,
    DOCKER,
    SINGULARITY,)
from .container_tasks import (
    run_docker_container_command,
    run_singularity_container_command,)
from .executable_tasks import run_executable_command


@shared_task
def run_task(uuid,
             task_class,
             command_to_run,
             env_vars_list,
             args_dict,
             **task_class_kwargs):
    """Launch an instance's job.

    This is the main function used to launch all tasks instance jobs.

    Args:
        uuid: A string containing the uuid of the job being run.
        task_class: A string defined in the constants module resprenting
            one of the task classes.
        command_to_run: A string containing the command to run.
        env_vars_list: A list of strings containing the environment
            variable names for the worker to consume from its
            environment.
        args_dict: A dictionary containing arguments and corresponding
            values.
        **task_class_kwargs: Arbitrary keywords arguments containing
            variables specific to the class of the task.

            For container task types you should be passing in

            logs_path: A string (or None) containing the path of the
                directory in the container containing the logs.
            results_path: A string (or None) containing the path of the
                directory in the container containing any output files.
            container_image: A string containing the name of the
                container to pull.
            container_type: A string defined in the constants module
                representing the type of container.

    Raises:
        NotImplementedError: An unsupported container type was passed
            in.
    """
    # Determine which class of task to run
    if task_class == CONTAINER_TASK:
        # Unpack some variables
        logs_path = task_class_kwargs["logs_path"]
        results_path = task_class_kwargs["results_path"]
        container_image = task_class_kwargs["container_image"]
        container_type = task_class_kwargs["container_type"]

        # Determine whether to run a Docker or Singularity container
        if container_type == DOCKER:
            return run_docker_container_command(
                uuid=uuid,
                container_image=container_image,
                command_to_run=command_to_run,
                logs_path=logs_path,
                results_path=results_path,
                env_vars_list=env_vars_list,
                args_dict=args_dict,)

        if container_type == SINGULARITY:
            return run_singularity_container_command(
                uuid=uuid,
                container_image=container_image,
                command_to_run=command_to_run,
                logs_path=logs_path,
                results_path=results_path,
                env_vars_list=env_vars_list,
                args_dict=args_dict,)

        # Container type passed in is not supported!
        raise NotImplementedError(
            "Unsupported container type {}".format(container_type))
    elif task_class == EXECUTABLE_TASK:
        return run_executable_command(
            uuid=uuid,
            command_to_run=command_to_run,
            env_vars_list=env_vars_list,
            args_dict=args_dict,)
    else:
        # Task class passed in is not supported!
        raise NotImplementedError(
            "Unsupported task class {}".format(task_class))


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
        r'/api/updatetaskinstancestatus/',
        job_uuid,)
    endpoint_url = '/'.join(s.strip('/') for s in endpoint_url_pieces) + '/'

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
    update_job(api_token=os.environ['API_AUTH_TOKEN'],
               job_uuid=str(kwargs['headers']['id']),
               state=PUBLISHED,)


@task_prerun.connect
def task_prerun_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['API_AUTH_TOKEN'],
               job_uuid=str(kwargs['task_id']),
               state=RUNNING,)


@task_success.connect
def task_success_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['API_AUTH_TOKEN'],
               job_uuid=kwargs['sender'].request.id,
               state=SUCCESSFUL,)


@task_failure.connect
def task_failure_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['API_AUTH_TOKEN'],
               job_uuid=kwargs['task_id'],
               state=FAILED,)


@task_revoked.connect
def task_revoked_handler(**kwargs):
    """Update the state of the task instance.

    Arg:
        kwargs: A dictionary containing information about the task
            instance.
    """
    update_job(api_token=os.environ['API_AUTH_TOKEN'],
               job_uuid=kwargs['request'].task_id,
               state=TERMINATED,)
