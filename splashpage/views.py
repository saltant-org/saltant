"""Views for the splash page."""

import os
from django.shortcuts import render

# Create your views here.
def splash_page_view(request):
    """Splash page for saltant."""
    # Build the context
    context = {}

    # Name of the project
    context['project_name'] = os.environ['PROJECT_NAME']

    return render(request, 'splash_page.html', context)
