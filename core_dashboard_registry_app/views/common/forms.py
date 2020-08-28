"""Forms for admin views
"""
from django import forms
from django_mongoengine.forms import DocumentForm

from core_main_app.components.data.models import Data


class EditDataForm(DocumentForm):
    """EditDataForm"""

    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new title"}
        ),
    )

    class Meta(object):
        document = Data
        fields = ["title"]
