from django import forms
from .models import Reporting, ModelReporting, Table, Value, Filter


class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        exclude = ['file']


class ModelReportingForm(forms.ModelForm):
    class Meta:
        model = ModelReporting
        exclude = ['created']


class TableForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = Table
        exclude = ['model_reporting', 'order']


class FilterForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = Filter
        exclude = ["content_type", "object_id", "item", "order", "format_data"]


class ValueForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = Value
        fields = ["value"]
