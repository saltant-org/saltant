"""Contains utility functions for other modules."""

import erron
import os


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
