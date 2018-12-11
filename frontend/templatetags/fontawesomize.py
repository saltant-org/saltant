"""Filter to convert booleans to icons."""

import json
from django.template import Library


register = Library()


@register.filter(is_safe=True)
def fontawesomize(val):
    """Convert boolean to font awesome icon."""
    if val:
        return '<i class="fa fa-check" style="color: green"></i>'

    return '<i class="fa fa-times" style="color: red"></i>'
