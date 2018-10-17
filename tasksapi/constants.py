"""Constants for the tasksapi app."""

# Choices for the task instance's state field. The states are based off
# of signals provided by Celery (which in fact set the state field):
# http://docs.celeryproject.org/en/master/userguide/signals.html.
CREATED = "created"
PUBLISHED = "published"
RUNNING = "running"
SUCCESSFUL = "successful"
FAILED = "failed"
TERMINATED = "terminated"

# Tuple of (key, display_name)s
STATE_CHOICES = (
    (CREATED, "created"),
    (PUBLISHED, "published"),
    (RUNNING, "running"),
    (SUCCESSFUL, "successful"),
    (FAILED, "failed"),
    (TERMINATED, "terminated"),
)

STATE_MAX_LENGTH = 10

# Choices for container types.
DOCKER = "docker"
SINGULARITY = "singularity"

# Tuple of (key, display_name)s
CONTAINER_CHOICES = ((DOCKER, "Docker"), (SINGULARITY, "Singularity"))

CONTAINER_TYPE_MAX_LENGTH = 11

# Choices for class of task
CONTAINER_TASK = "container"
EXECUTABLE_TASK = "executable"
