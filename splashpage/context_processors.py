"""Give common information to templates."""

import os


def export_env_vars(request):
    """Let templates know about the project name and base URL."""
    data = {}
    data['PROJECT_NAME'] = os.environ['PROJECT_NAME']
    data['DJANGO_BASE_URL'] = os.environ['DJANGO_BASE_URL']
    return data
