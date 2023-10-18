from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


CHOICE_FORMAT_FILE = [
    ('TXT', 'TXT'),
    ('RTF', 'RTF'),
    ('EXCEL', 'EXCEL'),
    ('CSV', 'CSV')
]
CHOICE_TABLE = [
    (i.model, i.model) for i in ContentType.objects.filter(app_label='data_reference')
]
CHOICE_FORMAT_DATA = [
    ('DATE', 'DATE'),
    ('DATETIME', 'DATETIME'),
    ('FLOAT', 'FLOAT'),
    ('INT', 'INT'),
    ('STRING', 'STRING')
]


class BaseReplacement(models.Model):
    table = models.CharField(choices=CHOICE_TABLE, max_length=100, default='')
    attr_name = models.CharField(max_length=100, default='')
    value = models.CharField(default='', max_length=100)
    format = models.CharField(choices=CHOICE_FORMAT_DATA, default='', max_length=100)

    class Meta:
        abstract = True


class BaseText(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class BaseRTF(BaseText):
    pass


class BaseExcel(models.Model):
    created = models.DateTimeField(auto_now_add=True)


class RegularExpression(models.Model):
    base_text = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in":
                ('basetext', 'basertf', 'baseexcel', 'cells')
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('base_text', 'object_id')
    expression = models.CharField(default='', max_length=255)
    comment = models.TextField(default='')
    is_splitter = models.BooleanField(default=False)
    previous_reg_exp = models.OneToOneField(
        'RegularExpression',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="next_reg_exp"
    )
    is_dependant = models.BooleanField(default=False)
    can_extract_data = models.BooleanField(default=True)

    def __str__(self):
        return self.expression


class ReplacementField(BaseReplacement):
    reg_expression = models.ForeignKey(RegularExpression, on_delete=models.CASCADE, related_name='reg_to_fields')


class Cells(models.Model):
    cell = models.CharField(default='', max_length=100)
    reg_expression = models.ForeignKey(
        RegularExpression,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reg_to_cells',
        limit_choices_to={
            'base_text__model__in': ('cells',)
        }
    )
    sheet_name = models.CharField(default='', max_length=100)
    base_excel = models.ForeignKey(
        'BaseExcel',
        on_delete=models.CASCADE,
        related_name='base_to_excel_cells'
    )
    previous_cell = models.OneToOneField(
        'Cells',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="next_cell"
    )
    order = OrderField(blank=True, for_fields=['base_excel'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.sheet_name + "!" + self.cell if self.sheet_name != '' else self.cell


class CellsReplacement(BaseReplacement):
    cell = models.ForeignKey(Cells, on_delete=models.CASCADE, related_name='cells_to_fields')


class ModelImportation(models.Model):
    format = models.CharField(choices=CHOICE_FORMAT_FILE, max_length=100)
    name = models.CharField(default='', max_length=100, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    table_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': ('basetext', 'basertf', 'baseexcel', 'cells')
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('table_type', 'object_id')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [
            ['name', 'format']
        ]


def import_upload_directory(instance, filename):
    queryset = Importation.objects.all()
    index = 1 if len(queryset) == 0 else queryset.last().pk
    return 'importation/{}/{}'.format(index, filename)


class Importation(models.Model):
    model_import = models.ForeignKey(ModelImportation, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=import_upload_directory)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class ConcernedTable(models.Model):
    model_import = models.ForeignKey(ModelImportation, on_delete=models.CASCADE, related_name='concerned_tables')
    linked_to = models.ForeignKey(
        'ConcernedTable',
        on_delete=models.SET_NULL,
        related_name='linked_to_table',
        null=True,
        blank=True
        )
    concerned_table = models.CharField(choices=CHOICE_TABLE, max_length=100)

    def __str__(self):
        return self.concerned_table
