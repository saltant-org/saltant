"""A widget using JSONEditor."""

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class JSONEditorWidget(forms.Widget):
    """A widget using JSONEditor.

    See https://github.com/josdejong/jsoneditor.
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
