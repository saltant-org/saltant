"""Give common information to templates."""

import os


def export_env_vars(_):
    """Let templates know about common things."""
    data = {}
    data["DJANGO_BASE_URL"] = os.environ["DJANGO_BASE_URL"]
    data["FLOWER_URL"] = os.environ["FLOWER_URL"]
    data["PROJECT_NAME"] = os.environ["PROJECT_NAME"]
    data["PROJECT_USES_ROLLBAR"] = os.environ["PROJECT_USES_ROLLBAR"]
    data["RABBITMQ_MANAGEMENT_URL"] = os.environ["RABBITMQ_MANAGEMENT_URL"]
    data["ROLLBAR_PROJECT_URL"] = os.environ["ROLLBAR_PROJECT_URL"]
    return data
