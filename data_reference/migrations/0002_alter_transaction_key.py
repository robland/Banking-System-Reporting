# Generated by Django 4.0.3 on 2022-04-17 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_reference', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='key',
            field=models.CharField(max_length=17),
        ),
    ]
