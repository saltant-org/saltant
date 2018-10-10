"""Contains task functionality for container-based tasks.

Note that none of these functions themselves are registered with Celery;
instead they are used by other functions which *are* registered with
Celery.
"""

import json
import os
import shlex
import timeout_decorator
from .utils import create_local_directory


class SingularityPullFailure(Exception):
    """An error for when Singularity pulls fail."""
    pass


def run_docker_container_command(uuid,
                                 container_image,
                                 command_to_run,
                                 logs_path,
                                 results_path,
                                 env_vars_list,
                                 args_dict):
    """Launch an executable within a Docker container.

    Args:
        uuid: A string containing the uuid of the job being run.
        container_image: A string containing the name of the container
            to pull.
        command_to_run: A string containing the command to run.
        logs_path: A string (or None) containing the path of the
            directory containing the relevant logs within the container.
        results_path: A string (or None) containing the path of the
            directory containing any output files from the container.
        env_vars_list: A list of strings containing the environment
            variable names for the worker to consume from its
            environment.
        args_dict: A dictionary containing arguments and corresponding
            values.

    Raises:
        KeyError: An environment variable specified was not available in
            the worker's environment.
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

    # Find out where to put the logs
    if logs_path is None:
        volumes_dict = {}
    else:
        host_logs_path = os.path.join(
            os.environ['WORKER_LOGS_DIRECTORY'],
            uuid,)
        volumes_dict = {host_logs_path: {'bind': logs_path, 'mode': 'rw'},}

    # Find out where to put the results
    if results_path is not None:
        host_results_path = os.path.join(
            os.environ['WORKER_RESULTS_DIRECTORY'],
            uuid,)
        volumes_dict[host_results_path] = {
            'bind': results_path,
            'mode': 'rw',}

    # Consume necessary environment variables
    try:
        environment = {key: os.environ[key] for key in env_vars_list}
    except KeyError as e:
        raise KeyError(
            "Environment variable %s not present in the worker's environment!"
            % e)

    # Also pass along the job's UUID
    environment['JOB_UUID'] = uuid

    # Compose the command to run
    if args_dict:
        command = "{executable} '{args}'".format(
            executable=command_to_run,
            args=json.dumps(args_dict))
    else:
        command = command_to_run

    # Run the executable
    client.containers.run(
        image=container_image,
        command=command,
        environment=environment,
        volumes=volumes_dict,)


def run_singularity_container_command(uuid,
                                      container_image,
                                      command_to_run,
                                      logs_path,
                                      results_path,
                                      env_vars_list,
                                      args_dict,):
    """Launch an executable within a Singularity container.

    Args:
        uuid: A string containing the uuid of the job being run.
        container_image: A string containing the name of the container
            to pull.
        command_to_run: A string containing the command to run.
        logs_path: A string (or None) containing the path of the
            directory containing the relevant logs within the container.
        results_path: A string (or None) containing the path of the
            directory containing any output files from the container.
        env_vars_list: A list of strings containing the environment
            variable names for the worker to consume from its
            environment.
        args_dict: A dictionary containing arguments and corresponding
            values.

    Raises:
        KeyError: An environment variable specified was not available in
            the worker's environment.
        SingularityPullFailure: The Singularity pull could not complete
            with the specified timeout and number of retries.
    """
    # Import Singularity library
    from spython.main import Client as client

    # Pull the specified container. This pull in the latest version of
    # the container (with the specified tag if provided).
    timeout = int(os.environ['SINGULARITY_PULL_TIMEOUT'])
    num_retries = int(os.environ['SINGULARITY_PULL_RETRIES'])

    # Put a timeout on the client pull method
    client.pull = timeout_decorator.timeout(
        timeout,
        timeout_exception=StopIteration)(client.pull)

    for retry in range(num_retries):
        try:
            singularity_image = client.pull(
                image=container_image,
                pull_folder=os.environ['WORKER_SINGULARITY_IMAGES_DIRECTORY'],
                name_by_commit=True,)

            break
        except StopIteration:
            # If this is the last retry, raise an exception to indicate
            # a failed job
            if retry == num_retries - 1:
                raise SingularityPullFailure(
                    ("Could not pull {image_url} within "
                     "{timeout} seconds after {num_retries} retries.").format(
                         image_url=container_image,
                         timeout=timeout,
                         num_retries=num_retries),)

    # Find out where to put the logs
    if logs_path is None:
        bind_option = []
    else:
        # Create the host logs path. This is required by the Singularity
        # library (though not the Docker library)
        host_logs_path = os.path.join(
            os.environ['WORKER_LOGS_DIRECTORY'],
            uuid,)

        create_local_directory(host_logs_path)

        # Build the bind option to pass on to Singularity
        bind_option = [host_logs_path.rstrip('/')
                       + ":"
                       + logs_path.rstrip('/')]

    # Find out where to put the results
    if results_path is not None:
        # Create the host results path
        host_results_path = os.path.join(
            os.environ['WORKER_RESULTS_DIRECTORY'],
            uuid,)

        create_local_directory(host_results_path)

        # Build the bind option to pass on to Singularity
        bind_option += [host_results_path.rstrip('/')
                        + ":"
                        + results_path.rstrip('/')]

    # Check for required environment variables. Note that by default
    # Singularity containers have access to their outside environment
    # variables, so we don't need to pass them along explicitly like we
    # need to for a Docker container.
    try:
        # Test to see that all keys are defined
        {key: os.environ[key] for key in env_vars_list}
    except KeyError as e:
        raise KeyError(
            "Environment variable %s not present in the worker's environment!"
            % e)

    # Pass along the job's UUID
    os.environ['JOB_UUID'] = uuid

    # Compose the command to run
    command = shlex.split(command_to_run)

    if args_dict:
        command += [json.dumps(args_dict)]

    # Run the executable
    iter_ = client.execute(
        image=singularity_image,
        command=command,
        bind=bind_option,
        stream=True,)

    # Okay, here's some magic. The issue is that without stream=True in
    # the above call, there's no way of determining the return code of
    # the above operation, and so no way of knowing whether it failed.
    # However, with stream=True, it'll raise a
    # subprocess.CalledProcessError exception for any non-zero return
    # code. Great! But before we can get that exception triggered we
    # need to iterate through all of the command's stdout, which is what
    # the below (seemingly useless) loop does.
    for _ in iter_:
        pass
