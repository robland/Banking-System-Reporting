from django.contrib import admin
from .models import *


@admin.register(ModelImportation)
class ModelImportationAdmin(admin.ModelAdmin):
    list_display = ['name', 'format', 'table_type', 'object_id', 'created']
    list_filter = ['format']


@admin.register(ReplacementField)
class ReplacementFieldAdmin(admin.ModelAdmin):
    list_display = ['table', 'attr_name', 'value', 'reg_expression']
    list_filter = ['table']


@admin.register(BaseText)
class BaseTextAdmin(admin.ModelAdmin):
    list_display = ['created']


@admin.register(BaseExcel)
class BaseExcelAdmin(admin.ModelAdmin):
    list_display = ['created']


@admin.register(BaseRTF)
class BaseRTFAdmin(admin.ModelAdmin):
    list_display = ['created']


@admin.register(Cells)
class CellsAdmin(admin.ModelAdmin):
    list_display = ['order', 'sheet_name', 'cell', 'previous_cell', 'reg_expression', 'base_excel']


@admin.register(RegularExpression)
class RegularExpressionAdmin(admin.ModelAdmin):
    list_display = [
        'base_text', 'expression', 'is_splitter', 'can_extract_data', 'is_dependant', 'previous_reg_exp', 'comment'
    ]


@admin.register(CellsReplacement)
class CellsReplacement(admin.ModelAdmin):
    list_display = ['table', 'attr_name', 'value', 'cell']
    list_filter = ['table']


@admin.register(Importation)
class ImportationAdmin(admin.ModelAdmin):
    list_display = ['file', 'model_import', 'created']


@admin.register(ConcernedTable)
class ConcernedTableAdmin(admin.ModelAdmin):
    list_display = ['model_import', 'concerned_table', 'linked_to']
