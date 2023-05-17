from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from datetime import datetime
from django.urls import reverse_lazy

from .models import SearchOptions


class SearchForms(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy("dashboard:index")
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = SearchOptions
        fields = ('name', 'city', 'region', 'activity_type', 'exclude_no_email')

    def save(self, commit=True):
        search = super().save(commit=False)
        if commit:
            search.save()
        return search
