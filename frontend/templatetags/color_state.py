"""Add background color to a status."""

import json
from django.template import Library
from frontend.constants import STATE_COLOR_LIGHTER_DICT


register = Library()


@register.filter(is_safe=True)
def color_state(state):
    """Add background colour to state text."""
    return (
        '<span style="background-color: %s; padding: 0 0.169em;">%s</span>'
        % (STATE_COLOR_LIGHTER_DICT[state], state)
    )
