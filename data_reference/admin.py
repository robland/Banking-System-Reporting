from django.contrib import admin
from .models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['agency', 'key', 'debit', 'credit']
    search_fields = ['key']


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['number', 'product', 'name', 'account', 'created']


@admin.register(ModelTable)
class ModelTableAdmin(admin.ModelAdmin):
    list_display = ['title', 'model_name', 'created']


@admin.register(ModelColumn)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_table', 'created']
