"""Celery app settings."""

from __future__ import absolute_import  # for Python 2.x workers
from celery import Celery
from saltant import settings
from tasksapi.tasks import run_task


# Run the celery app
app = Celery("saltant")

# Set the config options specified in settings
app.conf.update(
    broker_pool_limit=settings.CELERY_BROKER_POOL_LIMIT,
    broker_url=settings.CELERY_BROKER_URL,
    timezone=settings.CELERY_TIMEZONE,
)

# Set SSL setting if we're using SSL
try:
    app.conf.update(broker_use_ssl=settings.BROKER_USE_SSL)
except AttributeError:
    pass

# Let Rollbar report Celery worker errors (see
# https://www.mattlayman.com/2017/django-celery-rollbar.html)
if settings.PROJECT_USES_ROLLBAR and settings.IM_A_CELERY_WORKER:
    from celery.signals import task_failure
    import rollbar

    rollbar.init(**settings.ROLLBAR)

    def celery_base_data_hook(request, data):
        data["framework"] = "celery"

    rollbar.BASE_DATA_HOOK = celery_base_data_hook

    @task_failure.connect
    def handle_task_failure(**kw):
        rollbar.report_exc_info(extra_data=kw)
