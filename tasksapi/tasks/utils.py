"""Contains utility functions for tasks."""

import errno
import os
import sys


def create_local_directory(path):
    """Create a local directory as in mkdir_p.

    Replace this function with os.makedirs(path, exist_ok=True) when
    support for Python 2.7 is deprecated.
    """
    if sys.version_info.major >= 3 and sys.version_info.minor >= 2:
        # Use standard library functionality for Python 3
        os.makedirs(path, exist_ok=True)
    else:
        # For Python < 3.2, the exist_ok argument for the above
        # function doesn't exist
        mkdir_p(path)


def mkdir_p(path):
    """Emulate mkdir -p.

    There's not built-in for this with Python 2, so have to write a
    custom function for it. Thanks to Chris for his answer at
    StackOverflow at
    https://stackoverflow.com/questions/9079036/detect-python-version-at-runtime.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
