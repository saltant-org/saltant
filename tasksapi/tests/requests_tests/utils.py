"""Contains helpers for requests tests."""

from tasksapi.constants import DOCKER


TEST_CONTAINER_TASK_TYPE_DICT = dict(
    name="my-task-type",
    description="Fantastic task type",
    container_image="mwiens91/hello-world",
    container_type=DOCKER,
    command_to_run="/app/hello_world.py",
    logs_path="/logs/",
    results_path="/results/",
    environment_variables=["HOME"],
    required_arguments=["name"],
    required_arguments_default_values={"name": "AzureDiamond"},
)

TEST_EXECUTABLE_TASK_TYPE_DICT = dict(
    name="my-task-type",
    description="Fantastic task type",
    command_to_run="true",
    environment_variables=["HOME"],
    required_arguments=["name"],
    required_arguments_default_values={"name": "AzureDiamond"},
)
