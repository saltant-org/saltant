"""Constants for the tasks app."""

# Choices for the task instance's state field. The states are based off
# of signals provided by Celery (which in fact set the state field):
# http://docs.celeryproject.org/en/master/userguide/signals.html.  The
# choices should be no longer than  the number of characters allowed by
# the task instance's state CharField (which has a max length of 7 as of
# 2018-06-24).
CREATED = 'CREATED'
PUBLISHED = 'PUBLISH'
RUNNING = 'RUNNING'
SUCCESSFUL = 'SUCCESS'
FAILED = 'FAIL'
REVOKED = 'REVOKED'
