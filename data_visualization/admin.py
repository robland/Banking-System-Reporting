from django.contrib import admin
from .models import *


@admin.register(ModelDashBoard)
class ModelDashBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment']


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ['model_dashboard', 'child']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'container']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["widget", "data"]


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ["widget", "data"]


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ["widget", "label", "data"]
