from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from data_importation.models import *
from banking_reporting_system.settings import MEDIA_ROOT
import re
from .utils_functions import *
from .models import BaseText


"""@receiver(post_save, sender=Importation)
def test_extraction(sender, instance, **kwargs):
    extract_data_from(instance)
"""


@receiver(pre_save, sender=ModelImportation)
def create_base_format(sender, instance, **kwargs):
    base = None
    if instance.format in ['TXT', 'RTF']:
        base = "basetext"
    elif instance.format in ["EXCEL"]:
        base = "baseexcel"
    model_type = ContentType.objects.get(app_label='data_importation', model=base)

    instance.table_type = model_type
    base_obj = model_type.model_class().objects.create()
    instance.object_id = base_obj.pk
    return instance


@receiver(pre_save, sender=RegularExpression)
def link_base_to_reg_expression(sender, instance, **kwargs):
    pass


@receiver(pre_delete, sender=ModelImportation)
def after_deleting_model_importation(sender, instance, **kwargs):
    instance.item.delete()


@receiver(pre_delete, sender=Cells)
def after_deleting_cell(sender, instance, **kwargs):
    instance.reg_expression.delete()

