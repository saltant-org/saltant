"""Constants for the tasksapi app."""

# Choices for the task instance's state field. The states are based off
# of signals provided by Celery (which in fact set the state field):
# http://docs.celeryproject.org/en/master/userguide/signals.html.  The
# choices should be no longer than  the number of characters allowed by
# the task instance's state CharField (which has a max length of 10 as
# of 2018-07-02).
CREATED = 'created'
PUBLISHED = 'published'
RUNNING = 'running'
SUCCESSFUL = 'successful'
FAILED = 'failed'
TERMINATED = 'terminated'

# Choices for container types. Limited to 11 characters as of
# 2018-07-04.
DOCKER = 'docker'
SINGULARITY = 'singularity'
