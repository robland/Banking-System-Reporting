from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from data_importation.fields import OrderField


class DashBoard(models.Model):
    model_dashboard = models.OneToOneField(
        'ModelDashBoard',
        on_delete=models.SET_NULL,
        related_name='model_to_dashboard',
        null=True
    )


class ModelDashBoard(models.Model):
    name = models.CharField(default='', max_length=100)
    comment = models.TextField(default='')

    def __str__(self):
        return self.name


class Container(models.Model):
    model_dashboard = models.ForeignKey(
        ModelDashBoard,
        on_delete=models.CASCADE,
        related_name='model_dashboard_to_containers'
    )
    child = models.ForeignKey(
        'Container',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='father_to_children'
    )


class Widget(models.Model):
    title = models.CharField(max_length=100, default="")
    content_type = models.OneToOneField(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('table', 'chart', 'value')
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField('object_id')
    container = models.ForeignKey(
        'Container',
        on_delete=models.CASCADE,
        related_name="container_to_widgets"
    )


class Table(models.Model):
    data = models.JSONField()
    widget = models.OneToOneField(
        Widget,
        on_delete=models.SET_NULL,
        null=True,
        related_name='container_to_tables'
    )


class Chart(models.Model):
    data = models.JSONField()
    widget = models.OneToOneField(
        Widget,
        on_delete=models.SET_NULL,
        null=True,
        related_name='container_to_charts'
    )


class Value(models.Model):
    data = models.JSONField()
    label = models.CharField(max_length=100, default='')
    widget = models.OneToOneField(
        Widget,
        on_delete=models.SET_NULL,
        null=True,
        related_name='container_to_values'
    )
