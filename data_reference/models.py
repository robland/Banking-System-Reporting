from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Amount:
    def __init__(self):
        self.dict_attr = dict()

    def create_function(self, **dict_attr):
        dict_attr['debit'] = 0 if not dict_attr['debit'].strip() else float(''.join(dict_attr['debit'].strip()
                                                                                    .split('.')))
        dict_attr['credit'] = 0 if not dict_attr['credit']\
            .strip() else float(''.join(dict_attr['credit'].strip().split('.')))
        # dict_attr['label'] = dict_attr['label'].strip()
        # dict_attr['class_name'] = dict_attr['class_name'].strip()
        self.dict_attr = dict_attr
        return dict_attr


class Transaction(models.Model, Amount):
    debit = models.FloatField(default=0, null=True)
    credit = models.FloatField(default=0, null=True)
    agency = models.ForeignKey('Agency',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    key = models.CharField(max_length=17)
    created = models.DateTimeField(auto_now_add=True)



class Balance(models.Model, Amount):
    class_name = models.CharField(default='', max_length=6)
    label = models.CharField(default='', max_length=100)
    debit = models.FloatField(default=0)
    credit = models.FloatField(default=0)


class Agency(models.Model):
    code = models.CharField(default='', max_length=100)
    name = models.CharField(default='', max_length=100)

    def create_function(self, **attr_dict):
        return attr_dict

    def __str__(self):
        return ' '.join([self.code, self.name])


class Card(models.Model):
    number = models.CharField(default='', max_length=17)
    product = models.CharField(default='', max_length=100)
    name = models.CharField(default='', max_length=255)
    account = models.CharField(default='', max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def create_function(self, **attr_dict):
        return attr_dict


class ModelTable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(default='', max_length=100)
    model_name = models.CharField(default='', max_length=100)


class ModelColumn(models.Model):
    name = models.CharField(default='', max_length=100)
    model_table = models.ForeignKey(
        ModelTable,
        on_delete=models.CASCADE,
        related_name='table_to_fields',

    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'model_table']
