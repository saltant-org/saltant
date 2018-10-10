"""Contains task functionality for executable-based tasks.

Note that none of these functions themselves are registered with Celery;
instead they are used by other functions which *are* registered with
Celery.
"""

import json
import os
import shlex
import subprocess
from .utils import create_local_directory


def run_executable_command(uuid,
                           command_to_run,
                           env_vars_list,
                           args_dict,):
    """Launch an executable within a Docker container.

    Args:
        uuid: A string containing the uuid of the job being run.
        command_to_run: A string containing the command to run.
        env_vars_list: A list of strings containing the environment
            variable names for the worker to consume from its
            environment.
        args_dict: A dictionary containing arguments and corresponding
            values.

    Raises:
        KeyError: An environment variable specified was not available in
            the worker's environment.
        subprocess.CalledProcessError: The process returned with a
            non-zero code.
    """
    # Set up the host log directory for the job
    host_logs_path = os.path.join(
        os.environ['WORKER_LOGS_DIRECTORY'],
        uuid,)

    create_local_directory(host_logs_path)

    # Build paths to stdout and stdin files
    host_stdout_log_path = os.path.join(
        host_logs_path,
        uuid + '-' + 'stdout.txt',)

    host_stderr_log_path = os.path.join(
        host_logs_path,
        uuid + '-' + 'stderr.txt',)

    # Consume necessary environment variables
    try:
        environment = {key: os.environ[key] for key in env_vars_list}
    except KeyError as e:
        raise KeyError(
            "Environment variable %s not present in the worker's environment!"
            % e)

    # Also pass along the job's UUID
    environment['JOB_UUID'] = uuid

    # And PATH
    try:
        environment['PATH'] = os.environ['PATH']
    except KeyError:
        # Okay, no path defined. No big deal
        pass

    # Run the command
    with open(host_stdout_log_path, 'w') as f_stdout:
        with open(host_stderr_log_path, 'w') as f_stderr:
            # Interpret the command to run: split the string into
            # substrings "naturally" (see Python's shlex library); and
            # try to process anything that looks like an environment
            # variable.
            command_to_run = os.path.expandvars(command_to_run)
            cmd_list = shlex.split(command_to_run)

            # Add in arguments if we have any
            if args_dict:
                cmd_list += [json.dumps(args_dict)]

            # Run command
            subprocess.check_call(
                args=cmd_list,
                stdout=f_stdout,
                stderr=f_stderr,
                env=environment,)
