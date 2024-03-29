# Generated by Django 4.0.3 on 2022-06-05 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_importation', '0007_alter_cellsreplacement_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cellsreplacement',
            name='table',
            field=models.CharField(choices=[('agency', 'agency'), ('balance', 'balance'), ('card', 'card'), ('modelcolumn', 'modelcolumn'), ('modeltable', 'modeltable'), ('transaction', 'transaction')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='concernedtable',
            name='concerned_table',
            field=models.CharField(choices=[('agency', 'agency'), ('balance', 'balance'), ('card', 'card'), ('modelcolumn', 'modelcolumn'), ('modeltable', 'modeltable'), ('transaction', 'transaction')], max_length=100),
        ),
        migrations.AlterField(
            model_name='replacementfield',
            name='table',
            field=models.CharField(choices=[('agency', 'agency'), ('balance', 'balance'), ('card', 'card'), ('modelcolumn', 'modelcolumn'), ('modeltable', 'modeltable'), ('transaction', 'transaction')], default='', max_length=100),
        ),
    ]
