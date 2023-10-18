from rest_framework.serializers import ModelSerializer
from .models import Importation


class ImportationSerializer(ModelSerializer):

    class Meta:
        model = Importation
        fields = ['model_import', 'filename', 'created']