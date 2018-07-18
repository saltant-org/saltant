"""Contains tasks to register with Celery."""

import json
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
    CREATED,
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
    DOCKER,
    SINGULARITY,)


def run_docker_container_executable(uuid,
                                    container_image,
                                    executable_path,
                                    logs_path,
                                    args_dict):
    """Launch an executable within a Docker container.

    Args:
        uuid: A string containing the uuid of the job being run.
        container_image: A string containing the name of the container
            to pull.
        executable_path: A string containing the path of the executable
            to execute within the container.
        logs_path: A string (or None) containing the path of the
            directory containing the relevant logs within the container.
        args_dict: A dictionary containing arguments and corresponding
            values.
    """
    # Import Docker. Useful to just import it here if we want to have
    # workers which *only* can support Singularity.
    import docker

    # Get the Docker client on the host machine (see
    # https://docker-py.readthedocs.io/en/stable/client.html#docker.client.from_env)
    client = docker.from_env()

    # Pull the Docker container. This pull in the latest version of the
    # container (with the specified tag if provided).
    client.images.pull(container_image)

    # Run the executable with the arguments
    if logs_path is None:
        volumes_dict = {}
    else:
        host_path = os.path.join(os.environ['WORKER_LOGS_DIRECTORY'], uuid)
        volumes_dict = {host_path: {'bind': logs_path, 'mode': 'rw'},}

    client.containers.run(
        image=container_image,
        command="{executable} '{args}'".format(
            executable=executable_path,
            args=json.dumps(args_dict)),
        volumes=volumes_dict,)


def run_singularity_container_executable(uuid,
                                         container_image,
                                         executable_path,
                                         logs_path,
                                         args_dict):
    """Launch an executable within a Singularity container.

    Args:
        uuid: A string containing the uuid of the job being run.
        container_image: A string containing the name of the container
            to pull.
        executable_path: A string containing the path of the executable
            to execute within the container.
        logs_path: A string (or None) containing the path of the
            directory containing the relevant logs within the container.
        args_dict: A dictionary containing arguments and corresponding
            values.
    """
    # Import Singularity library
    from spython.main import Client as client

    # Pull the specified container. This pull in the latest version of
    # the container (with the specified tag if provided).
    singularity_image = client.pull(
        image=container_image,
        pull_folder=os.environ['WORKER_SINGULARITY_IMAGES_DIRECTORY'],)

    # Run the executable with the arguments
    if logs_path is None:
        bind_option = None
    else:
        # Create the host path. This is required by the Singularity
        # library (though not the Docker library)
        host_path = os.path.join(os.environ['WORKER_LOGS_DIRECTORY'], uuid)
        os.makedirs(host_path, exist_ok=True)

        # Build the bind option to pass on to Singularity
        bind_option = host_path.rstrip('/') + ":" + logs_path.rstrip('/')

    client.execute(
        image=singularity_image,
        command=[executable_path, json.dumps(args_dict)],
        bind=bind_option,)


@shared_task
def run_task(uuid,
             container_image,
             container_type,
             script_path,
             logs_path,
             args_dict):
    """Launch an instance's job.

    This is the main function used to launch all tasks instance jobs.

    Args:
        uuid: A string containing the uuid of the job being run.
        container_image: A string containing the name of the container
            to pull.
        container_type: A string which is either "docker" or
            "singularity".
        script_path: A string containing the path of the script to
            execute within the container.
        logs_path: A string (or None) containing the path of the
            directory containing the relevant logs within the container.
        args_dict: A dictionary containing arguments and corresponding
            values.
    """
    # Determine whether to run a Docker or Singularity container
    if container_type == DOCKER:
        return run_docker_container_executable(
            uuid=uuid,
            container_image=container_image,
            executable_path=script_path,
            logs_path=logs_path,
            args_dict=args_dict,)
    elif container_type == SINGULARITY:
        return run_singularity_container_executable(
            uuid=uuid,
            container_image=container_image,
            executable_path=script_path,
            logs_path=logs_path,
            args_dict=args_dict,)
    else:
        return "Unsupported container type {}".format(container_type)


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
