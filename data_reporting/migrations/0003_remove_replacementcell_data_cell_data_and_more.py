# Generated by Django 4.0.3 on 2022-04-12 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_reporting', '0002_alter_table_options_remove_table_cell_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replacementcell',
            name='data',
        ),
        migrations.AddField(
            model_name='cell',
            name='data',
            field=models.JSONField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='FieldToCompute',
        ),
        migrations.DeleteModel(
            name='ReplacementCell',
        ),
    ]
