from django import forms
from .models import *


class ModelTableForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = ModelTable
        fields = ['title', 'model_name']


class ModelColumnForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = ModelColumn
        fields = ['name']
