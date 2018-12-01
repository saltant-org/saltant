"""Filter to provide JSON dump transforms."""

import json
from django.template import Library


register = Library()


def jsonify(object):
    """Perform a naive JSON dump."""
    return json.dumps(object)


register.filter("jsonify", jsonify)
