from django import forms
from .models import *


class ImportForm(forms.ModelForm):

    class Meta:
        model = Importation
        exclude = ['model_import', ]


class ModelImportationForm(forms.Form):
    model_import = forms.CharField()


class ModelImportForm(forms.ModelForm):
    class Meta:
        model = ModelImportation
        fields = ['name', 'format']


class RegularExpressionForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = RegularExpression
        fields = ['expression', 'comment', 'is_splitter', 'is_dependant', 'can_extract_data', 'previous_reg_exp']


class CellForm(forms.ModelForm):

    class Meta:
        model = Cells
        fields = ['cell', 'sheet_name', 'previous_cell', ]


class CellsReplacementForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = CellsReplacement
        fields = ['table', 'attr_name', 'value', 'format']


class ReplacementForm(forms.ModelForm):
    next_action = forms.CharField()

    class Meta:
        model = ReplacementField
        fields = ['table', 'attr_name', 'value', 'format']


class DeleteForm(forms.Form):
    confirmation = forms.CharField()
    key = forms.CharField()


