# Generated by Django 4.0.3 on 2022-05-30 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_importation', '0004_alter_importation_model_import'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importation',
            old_name='filename',
            new_name='file',
        ),
    ]
