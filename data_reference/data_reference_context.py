from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from data_reference.models import ModelTable


def all_data_reference_models(request):
    tables = ContentType.objects.filter(app_label__icontains='data_reference').exclude(model__startswith='model')
    return {
        'models': tables,
        'all_models_tables': ModelTable.objects.all()
    }


