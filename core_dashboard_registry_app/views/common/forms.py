"""Forms for admin views
"""
from django import forms
from django.forms import ModelForm

from core_main_app.components.data.models import Data


class EditDataForm(ModelForm):
    """EditDataForm"""

    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Type the new title",
            }
        ),
    )

    class Meta:
        """Meta"""

        model = Data
        fields = ["title"]
