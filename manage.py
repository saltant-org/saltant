#!/usr/bin/env python3
import os
import sys
import warnings
import dotenv

if __name__ == "__main__":
    # Load environment variables from .env file
    with warnings.catch_warnings():
        warnings.filterwarnings("error")

        try:
            dotenv.read_dotenv()
        except UserWarning:
            raise FileNotFoundError("Could not find .env!")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saltant.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
