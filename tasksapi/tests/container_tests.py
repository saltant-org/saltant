"""Contains container task tests for the tasksapi."""

import os
import pathlib
import subprocess
import uuid
import docker
from django.conf import settings
from django.test import TestCase
from tasksapi.tasks import (
    run_docker_container_command,
    run_singularity_container_command,)


class TasksApiContainerTests(TestCase):
    """Test tasks functionality.

    Using the Docker container defined here:
    https://github.com/mwiens91/saltant-test-docker-container.
    """
    @classmethod
    def setUpTestData(cls):
        """Create some temporary directories to store job results."""
        # Generate the base path for this test
        base_dir_name = os.path.join(
            settings.BASE_DIR,
            'temp-test-' + str(uuid.uuid4()),)

        # Make the logs and singularity images directories
        logs_path = os.path.join(
            base_dir_name,
            'logs/',)
        results_path = os.path.join(
            base_dir_name,
            'results/',)
        singularity_path = os.path.join(
            base_dir_name,
            'images/',)
        pathlib.Path(logs_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(results_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(singularity_path).mkdir(parents=True, exist_ok=True)

        # Overload our environment variables to use our generated temp
        # storage directories
        os.environ['WORKER_LOGS_DIRECTORY'] = logs_path
        os.environ['WORKER_RESULTS_DIRECTORY'] = results_path
        os.environ['WORKER_SINGULARITY_IMAGES_DIRECTORY'] = singularity_path

    def tearDown(self):
        """Clean up directories made in setUpTestData."""
        # TODO: this command fails because the files that the Docker
        # container creates are owned by 'root'. Looked into this a bit,
        # but couldn't find a clean solution, so right now there's no
        # automatic cleanup :(
        #
        # Note that since first writing this, base_dir_name was an
        # object attribute and shutil was imported. To test this again,
        # implement the things I just mentioned again.
        #shutil.rmtree(self.base_dir_name)
        pass

    def test_docker_success(self):
        """Make sure Docker jobs work properly."""
        run_docker_container_command(
            uuid='test-docker-success-uuid',
            container_image='mwiens91/hello-world',
            command_to_run='/app/hello_world.py',
            logs_path='/logs/',
            results_path='/results/',
            env_vars_list=['SHELL',],
            args_dict={'name': 'AzureDiamond'},)

    def test_singularity_success(self):
        """Make sure Singularity jobs work properly."""
        run_singularity_container_command(
            uuid='test-singularity-success-uuid',
            container_image='docker://mwiens91/hello-world',
            command_to_run='/app/hello_world.py',
            logs_path='/logs/',
            results_path='/results/',
            env_vars_list=['SHELL',],
            args_dict={'name': 'AzureDiamond'},)

    def test_docker_failure(self):
        """Make sure Docker jobs that fail are noticed."""
        with self.assertRaises(docker.errors.ContainerError):
            run_docker_container_command(
                uuid='test-docker-failure-uuid',
                container_image='mwiens91/test-error-containers',
                command_to_run='/app/error_raise.py',
                logs_path=None,
                results_path=None,
                env_vars_list=[],
                args_dict={},)

    def test_singularity_failure(self):
        """Make sure Singularity jobs that fail are noticed."""
        with self.assertRaises(subprocess.CalledProcessError):
            run_singularity_container_command(
                uuid='test-docker-failure-uuid',
                container_image='shub://mwiens91/test-error-containers',
                command_to_run='/error_raise.py',
                logs_path=None,
                results_path=None,
                env_vars_list=[],
                args_dict={},)
