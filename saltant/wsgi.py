"""
WSGI config for saltant project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import warnings
import dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables from .env file
with warnings.catch_warnings():
    warnings.filterwarnings("error")

    try:
        dotenv.read_dotenv(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        )
    except UserWarning:
        raise FileNotFoundError("Could not find .env!")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saltant.settings")

application = get_wsgi_application()
