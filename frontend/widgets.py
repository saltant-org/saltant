"""Custom widgets for forms."""

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class JSONEditorWidget(forms.Widget):
    """A JSONField widget using JSONEditor.

    See https://github.com/josdejong/jsoneditor. Note that this code is
    mostly derived from django-json-widget
    (https://github.com/jmrivas86/django-json-widget), but has been
    stripped down to be more lightweight.
    """
    template_name = "frontend/widgets/json_editor.html"

    def __init__(self, attrs=None, mode="code"):
        """Add in the display mode."""
        super().__init__(attrs=attrs)
        self.mode = mode

    def render(self, name, value, attrs=None, renderer=None):
        """Render the JSONField as a JSONEditor widget."""
        context = {"data": value, "name": name, "mode": self.mode}

        return mark_safe(render_to_string(self.template_name, context))
