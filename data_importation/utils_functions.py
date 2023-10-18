from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from banking_reporting_system.settings import MEDIA_ROOT
from .models import Importation, ModelImportation, RegularExpression
import re
import pandas as pd
from striprtf.striprtf import rtf_to_text
from datetime import date, datetime


def put_in_good_format(field, value):
    if field.format == 'STRING':
        return str(value).strip()

    if field.format == 'INT':
        return int(value.strip())

    if field.format == 'FLOAT':
        return float(value.strip())

    if field.format == 'DATE':
        return date(value.strip())

    if field.format == 'DATETIME':
        return datetime(value.strip())


class ExcelDataExtractor:
    def __init__(self, instance):
        self.model_import = ModelImportation.objects.get(
            pk=instance.__dict__['model_import_id']
        )
        self.cell = self.model_import.table_type.model_class().objects.all().first().base_to_excel_cells.all().first()
        self.current_cell = None
        self.obj = None
        self.df = pd.read_excel(MEDIA_ROOT + instance.file.name)
        self.data = []
        self.data_dict = dict()
        self.recursive_extract_data()
        self.save_data()
        self.last_objects = []

    def pre_save_action(self, value):
        for field in self.current_cell.cells_to_fields.all():
            v = put_in_good_format(field, value[int(field.value)]) if isinstance(value, (tuple, list)) else value
            self.data_dict.setdefault(field.attr_name, v)
        return self.data_dict

    def recursive_extract_data(self):
        rows, cols = self.df.shape
        self.current_cell = self.cell
        self.obj = ContentType.objects.get(model=self.current_cell.cells_to_fields.all().first().table).model_class()()
        for row in range(0, rows):
            self.recursive_excel_extraction(row)

    def recursive_excel_extraction(self, row):
        rang_a = ord('A')
        col = ord(self.current_cell.cell) - rang_a
        reg_data = self.current_cell.reg_expression.expression
        list_data = re.compile(reg_data).findall(str(self.df.iloc[row][col]))
        model = ContentType.objects.get(model=self.current_cell.cells_to_fields.all().first().table).model_class()
        if len(list_data) > 0:
            self.pre_save_action(list_data[0])
        try:
            self.current_cell = self.current_cell.next_cell
            self.recursive_excel_extraction(row)
        except:
            from .models import Cells
            instance = model()
            print(self.data_dict.values())
            if self.data_dict:
                try:
                    last_object, created = model.objects.get_or_create(**self.data_dict)

                except:
                    pass

            try:
                self.current_cell = Cells.objects.get(
                    order=self.current_cell.order + 1
                )
            except ObjectDoesNotExist:
                self.current_cell = self.cell
            self.data_dict.clear()
            self.obj = ContentType.objects.get(
                model=self.current_cell.cells_to_fields.all().first().table).model_class()()

    def save_data(self):
        last_object = None
        the_last = None
        model = None

    @property
    def parsed_data(self):
        return self.data


class TextDataExtractor:
    def __init__(self, instance):
        self.model_import = ModelImportation.objects.get(
            pk=instance.__dict__['model_import_id']
        )
        # self.regex = self.model_import.table_type.model_class().objects.first().regs.all()[0]
        self.regex = RegularExpression.objects.filter(
            base_text=self.model_import.table_type,
            object_id=self.model_import.object_id
        )[0]
        self.data = []
        print(self.regex)
        with open(MEDIA_ROOT + instance.file.name, 'r', encoding='utf8') as f:
            list_string = []
            if instance.model_import.format == 'rtf':
                list_string.append(rtf_to_text(f.read()))
            elif instance.model_import.format == 'txt':
                list_string.append(f.read())

            print(list_string)
            self.recursive_extract_data(list_string, self.regex)

        self.save_data()

    def save_data(self):
        last_object = None
        the_last = None
        model = None
        for data_dict in self.data:
            for keys, value in data_dict.items():
                for t in value:
                    the_last = {fields.attr_name: t[int(fields.value)] for fields in keys.reg_to_fields.all()}
                    table = keys.reg_to_fields.all().first().table
                    model = ContentType.objects.get(model=table).model_class()
                    instance = model()
                    try:
                        last_object, created = model.objects.get_or_create(**instance.create_function(**the_last))
                    except:
                        pass

    def recursive_extract_data(self, list_string, regex):
        for string in list_string:

            if regex.is_splitter:
                current_list = re.compile(regex.expression).split(string)
                try:
                    next_regex = self.regex.next_reg_exp
                    self.recursive_extract_data(current_list, next_regex)
                except:
                    pass
            if regex.can_extract_data:
                new_list = re.compile(regex.expression).findall(string)
                self.data.append({regex: new_list})
                try:
                    next_regex = regex.next_reg_exp
                    self.recursive_extract_data(list_string, next_regex)
                except:
                    pass

    @property
    def parsed_data(self):
        return self.data


class RTFDataExtractor(TextDataExtractor):
    pass


class CSVDataExtractor:
    def __init__(self, instance):
        self.model_import = ModelImportation.objects.get(
            pk=instance.__dict__['model_import_id']
        )
        self.list_regex = self.model_import.table_type.model_class().objects.all().first().regs.all()
        self.data_dict = {}

    @property
    def parsed_data(self):
        return self.data_dict


def data_extraction_factory(instance):
    filepath = instance.file.name
    if filepath.endswith('xls') or filepath.endswith('xlsx'):
        return ExcelDataExtractor(instance)

    elif filepath.endswith('txt') or filepath.endswith('rtf'):
        return TextDataExtractor(instance)

    elif filepath.endswith('csv'):
        return CSVDataExtractor(instance)

    else:
        raise ValueError("Cannot extract data from {}".format(filepath))


def extract_data_from(instance):
    factory_object = None
    try:
        factory_object = data_extraction_factory(instance)
    except ValueError as e:
        print(e)
    return factory_object


