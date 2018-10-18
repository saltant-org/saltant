"""Contains executable task tests for the tasksapi.

These test (unlike the other tests as of 2018-08-27) are *very* basic
and should be expanded in the future.
"""

import os
import pathlib
import shutil
import subprocess
import uuid
from django.conf import settings
from django.test import TestCase
from tasksapi.tasks import run_executable_command


class TasksApiExecutableTests(TestCase):
    """Test container tasks functionality."""

    def setUp(self):
        """Create some temporary directories to store job results."""
        # Generate the base path for this test
        self.base_dir_name = os.path.join(
            settings.BASE_DIR, "temp-test-" + str(uuid.uuid4())
        )

        # Make the logs and singularity images directories
        logs_path = os.path.join(self.base_dir_name, "logs/")
        pathlib.Path(logs_path).mkdir(parents=True, exist_ok=True)

        # Overload our environment variables to use our generated temp
        # storage directories
        os.environ["WORKER_LOGS_DIRECTORY"] = logs_path

    def tearDown(self):
        """Clean up directories made in setUpTestData."""
        shutil.rmtree(self.base_dir_name)

    def test_executable_success(self):
        """Make sure executable jobs work properly."""
        run_executable_command(
            uuid="test-executable-success-uuid",
            command_to_run="echo $SHELL",
            env_vars_list=["SHELL"],
            args_dict={},
            json_file_option=None,
        )

    def test_executable_failure(self):
        """Make sure executable jobs that fail are noticed."""
        with self.assertRaises(subprocess.CalledProcessError):
            run_executable_command(
                uuid="test-executable-failure-uuid",
                command_to_run="false",
                env_vars_list=[],
                args_dict={},
                json_file_option=None,
            )

    def test_executable_json_file_option(self):
        """Make sure the JSON file option works."""
        # TODO(mwiens91): write an actual test that parses the
        # JSON-encoded file
        run_executable_command(
            uuid="test-executable-success-uuid",
            command_to_run="echo",
            env_vars_list=[],
            args_dict={"toy": "example"},
            json_file_option="--json-file",
        )
