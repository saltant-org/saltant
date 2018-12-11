"""Filter to provide JSON dump transforms."""

import json
from django.template import Library


register = Library()


@register.filter(is_safe=True)
def jsonify(val):
    """Perform a naive JSON dump."""
    return json.dumps(val)
