# Generated by Django 4.0.3 on 2022-06-08 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('data_reporting', '0004_rename_data_table_columns_table_table_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='field',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='filter',
            name='operator_string',
            field=models.CharField(choices=[('=', '='), ('<=', '<='), ('contains', 'contains'), ('icontains', 'icontains'), ('startswith', 'startswith'), ('endswith', 'endswith')], default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filter',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'app_label__icontains': 'data_reporting', 'model__in': ('cell', 'table', 'chart')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
