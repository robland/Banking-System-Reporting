# Generated by Django 4.0.3 on 2022-06-12 17:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data_reference', '0006_alter_modelcolumn_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
