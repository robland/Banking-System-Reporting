from django.contrib import admin
from .models import *


@admin.register(Reporting)
class ReportingAdmin(admin.ModelAdmin):
    list_display = ['model_reporting', 'name', 'file', 'created']


@admin.register(ModelReporting)
class ModelReportingAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'created']


"""@admin.register(FieldToCompute)
class FieldToComputeAdmin(admin.ModelAdmin):
    list_display = ['filter', 'name', 'field', 'calcul', 'created']
"""


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'name']


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ['filter', 'value']


"""@admin.register(ReplacementCell)
class ReplacementCell(admin.ModelAdmin):
    list_display = ['sheet_name', 'column', 'row', 'data']
"""


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ["order", "sheet_name", "cell", "model_reporting"]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["order", "title", "model_reporting"]


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ["order", "title", 'cell', "model_reporting"]


admin.site.register(BaseFieldToCompute)
