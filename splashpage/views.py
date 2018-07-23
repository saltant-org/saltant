"""Views for the splash page."""

import os
from django.shortcuts import render


def splash_page_view(request):
    """Splash page for saltant."""
    # Build the context
    context = {}

    # Relevant values from .env
    context['rollbar_project_url'] = os.environ['ROLLBAR_PROJECT_URL']
    context['rabbitmq_management_url'] = (
        os.environ['RABBITMQ_MANAGEMENT_URL'])
    context['flower_url'] = os.environ['FLOWER_URL']

    return render(request, 'splashpage/splash_page.html', context)
