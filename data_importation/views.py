from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializer import *
from .models import *
from .forms import *
from .utils_functions import extract_data_from


def delete(request, instance, delete_form):
    if delete_form.is_valid():
        confirmation = delete_form.cleaned_data['confirmation']
        key = delete_form.cleaned_data['key']
        if confirmation == "yes":
            instance.delete()


@method_decorator(csrf_exempt, name='dispatch')
class ImportationViewSet(viewsets.ModelViewSet):
    queryset = Importation.objects.all()
    serializer_class = ImportationSerializer
    permission_classes = []


@login_required
def import_data(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponse("File uploaded")
        else:
            print(form.errors)
            raise Http404
    imports = Importation.objects.all()
    models_import = [(i.pk, i.name) for i in ModelImportation.objects.all()]
    return render(request, 'data_importation/importation.html', locals())


@login_required
def data_extraction(request):
    instance = Importation.objects.get(pk=97)
    instance.model_import = ModelImportation.objects.get(pk=15)
    instance.save()
    extract_data_from(instance)
    """if request.method == 'POST':
        form = ModelImportationForm(request.POST)

        if form.is_valid():
            instance.model_import = ModelImportation.objects.get(pk=form.cleaned_data['model_import'])
            instance.save()
            try:
                extract_data_from(instance)
                return redirect(reverse_lazy('import_data:import_data'))
            except:
                return redirect(reverse_lazy('import_data:import_data'))"""
    return redirect(reverse_lazy('import_data:import_data'))


@login_required
def create_model_importation(request):
    models_importation = ModelImportation.objects.all()
    formats = CHOICE_FORMAT_FILE
    form = ModelImportForm()

    if request.method == 'POST':
        form = ModelImportForm(request.POST)

        if form.is_valid():
            model_importation = form.save()
            pk = model_importation.pk
            if model_importation.format in ['TXT', 'RTF', 'CSV']:
                return redirect(
                    reverse_lazy('import_data:create-regular-expression-for-other-format', kwargs={'pk': pk})
                )
            elif model_importation.format in ["EXCEL"]:
                return redirect(reverse_lazy('import_data:create-regular-expression', kwargs={'pk': pk}))
        else:
            return render(request, 'data_importation/create-model-importation.html', locals())
    return render(request, 'data_importation/create-model-importation.html', locals())


@login_required
def create_regular_expression(request, pk):
    form = RegularExpressionForm()
    cell_form = CellForm()
    base = ModelImportation.objects.get(pk=pk)
    item = ModelImportation.objects.get(pk=pk).item
    previous_reg = RegularExpression.objects.filter(object_id=item.id)
    previous_cell = Cells.objects.filter(base_excel_id=item.id)

    if request.method == 'POST':
        form = RegularExpressionForm(request.POST)
        cell_form = CellForm(request.POST)

        if form.is_valid() and cell_form.is_valid():
            obj = form.save(commit=False)
            cell_obj = cell_form.save(commit=False)

            obj.base_text = base.table_type
            obj.object_id = item.id
            obj.save()

            cell_obj.reg_expression = obj
            cell_obj.base_excel = base.table_type.model_class().objects.get(pk=item.id)
            cell_obj.save()

            if form.cleaned_data["next_action"] == "1":
                return redirect(reverse_lazy('import_data:create-regular-expression', kwargs={'pk': pk}))
            elif form.cleaned_data["next_action"] == "2":
                print(cell_obj.pk)
                return redirect(reverse_lazy('import_data:add_field_to_cell', kwargs={'pk': cell_obj.pk}))

            # Renvoyer à la page de détail des expressions régulières
            return redirect(reverse_lazy("import_data:detail-model-importation", kwargs={'pk': base.pk}))
        else:
            return render(request, 'data_importation/create-reg-expression.html', locals())

    return render(request, 'data_importation/create-reg-expression.html', locals())


@login_required
def create_regular_expression_for_other_format(request, pk):
    form = RegularExpressionForm()
    base = ModelImportation.objects.get(pk=pk)
    item = ModelImportation.objects.get(pk=pk).item
    previous_reg = RegularExpression.objects.filter(object_id=item.id)

    if request.method == 'POST':
        form = RegularExpressionForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.base_text = base.table_type
            obj.object_id = item.id
            obj.save()

            if form.cleaned_data["next_action"] == "1":
                return redirect(
                    reverse_lazy('import_data:create_regular_expression_for_other_format', kwargs={'pk': pk})
                )
            elif form.cleaned_data["next_action"] == "2":
                return redirect(reverse_lazy('import_data:add_field_to_cell', kwargs={'pk': obj.pk}))

            # Renvoyer à la page de détail des expressions régulières
            return redirect(reverse_lazy("import_data:detail-model-importation", kwargs={'pk': base.pk}))
        else:
            return render(request, 'data_importation/create-reg-expression.html', locals())

    return render(request, 'data_importation/create-reg-expression.html', locals())


@login_required
def add_field_to_cell(request, pk):
    form = CellsReplacementForm()
    cell = get_object_or_404(Cells, pk=pk)
    tables = [i.model for i in ContentType.objects.filter(app_label__icontains='data_reference')]
    model_import = get_object_or_404(ModelImportation, cell.base_excel.pk)
    formats = CHOICE_FORMAT_DATA
    if request.method == 'POST':
        form = CellsReplacementForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.cell = cell
            obj.save()
            next_action = form.cleaned_data["next_action"]
            if next_action == "1":
                # page d'ajout
                return render(request, 'data_importation/add-cell-replacement.html', locals())
                pass
            elif next_action == "2":
                return redirect(reverse_lazy("import_data:add_field_to_cell", kwargs={'pk': cell.pk}))
            else:
                # return HttpResponse("Données des cellules bien liées!!!!!!")
                return redirect(reverse_lazy("import_data:detail-model-importation", kwargs={'pk':model_import.pk}))
                # renvoi vers la page détaillée des cells replacement

    return render(request, 'data_importation/add-cell-replacement.html', locals())


@login_required
def add_field_to_regular_expression(request, pk):
    form = ReplacementForm
    reg = get_object_or_404(RegularExpression, pk=pk)
    tables = [i.model for i in ContentType.objects.filter(app_label__icontains='data_reference')]
    model_import = ModelImportation.objects.get(table_type=reg.base_text, object_id=reg.object_id)
    formats = CHOICE_FORMAT_DATA
    if request.method == 'POST':
        form = ReplacementForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.reg_expression = reg
            obj.save()
            next_action = form.cleaned_data["next_action"]
            if next_action == "1":
                # page d'ajout
                return render(request, 'data_importation/add-cell-replacement.html', locals())
                pass
            elif next_action == "2":
                return redirect(reverse_lazy("import_data:add_field_to_cell", kwargs={'pk': reg.pk}))
            else:
                return redirect(reverse_lazy("import_data:detail-model-importation", kwargs={'pk': model_import.pk}))
                # return HttpResponse("Données des cellules bien liées!!!!!!")
                # renvoi vers la page détaillée des cells replacement

    return render(request, 'data_importation/add-cell-replacement.html', locals())


@login_required
def all_models_importation(request):
    all_models = ModelImportation.objects.all()
    bases = [i for i in all_models]
    print(bases)
    return render(request, 'data_importation/all_models_importation.html', locals())

# Vues propres au model_importation


@login_required
def detail_model_importation(request, pk):
    formats = [i[0] for i in CHOICE_FORMAT_FILE if not i[0] == 'EXCEL']
    model_import = get_object_or_404(ModelImportation, pk=pk)
    base = model_import.item
    reg_expression = RegularExpression.objects.filter(base_text__model='basetext', object_id=base.pk)
    pk = pk
    print(formats, reg_expression, base)
    return render(request, 'data_importation/detail-model-importation.html', locals())


@login_required
def edit_model_importation(request, pk):
    model_import = get_object_or_404(ModelImportation, pk=pk)
    form = ModelImportForm(instance=model_import)
    formats = CHOICE_FORMAT_FILE

    if request.method == "POST":
        form = ModelImportForm(request.POST)

        if form.is_valid():
            obj = ModelImportation.objects.update(**form.cleaned_data)
            print(obj)
            return redirect(reverse_lazy('import_data:detail-model-importation', kwargs={'pk': model_import.pk}))
    return render(request, 'data_importation/edit-model-importation.html', locals())


@login_required
def delete_model_importation(request, pk):
    delete_form = DeleteForm()
    model_import = get_object_or_404(ModelImportation, pk=pk)
    if request.method == 'POST':
        delete_form = DeleteForm(request.POST)
        delete(request, model_import, delete_form)

    return redirect(reverse_lazy('import_data:all_models_importation'))


# Vues propres aux expressions régulières

@login_required
def detail_regular_expression(request, pk):
    regular_expression = get_object_or_404(RegularExpression, pk=pk)
    return render(request, 'data_importation/detail-reg-expression.html', locals())


@login_required
def edit_regular_expression(request, pk):
    cell = get_object_or_404(Cells, pk=pk)
    model_import = ModelImportation.objects.get(object_id=cell.base_excel.pk)

    cell_form = CellForm(instance=cell)
    form = RegularExpressionForm(instance=cell.reg_expression)
    if request.POST:
        cell_form = CellForm(request.POST)
        form = RegularExpressionForm(request.POST)
        if cell_form.is_valid() and form.is_valid():
            Cells.objects.update_or_create(**cell_form.cleaned_data)
            RegularExpression.objects.update_or_create(**{key: value for key, value in form.cleaned_data.items() if key != "next_action"})
            return redirect(reverse_lazy('importation:detail-model-importation', kwargs={'pk': model_import.pk}))

    return render(request, 'data_importation/edit-reg-expression.html', locals())


@login_required
def delete_regular_expression(request, pk):
    delete_form = DeleteForm()
    regular_expression = get_object_or_404(RegularExpression, pk=pk)
    if request.method == 'POST':
        delete_form = DeleteForm(request.POST)
        delete(request, regular_expression, delete_form)

    return redirect(reverse_lazy('import_data:all_models_importation'))


# Vues propres au remplissage des  tables


@login_required
def detail_field_to_cell(request, pk):
    cell = get_object_or_404(CellsReplacement, pk=pk)
    return render(request, 'data_importation/detail-field-to-cell.html', locals())


@login_required
def edit_field_to_cell(request, pk):
    cell = get_object_or_404(CellsReplacement, pk=pk)
    return render(request, 'data_importation/create-field-to-cell.html', locals())


@login_required
def delete_field_to_cell(request, pk):
    delete_form = DeleteForm()
    cell = get_object_or_404(CellsReplacement, pk=pk)
    if request.method == 'POST':
        delete_form = DeleteForm(request.POST)
        delete(request, cell, delete_form)
    return redirect(reverse_lazy('import_data:all_models_importation'))


@login_required
def delete_base_cell(request, pk):
    delete_form = DeleteForm()
    cell = get_object_or_404(Cells, pk=pk)
    base = cell.base_excel
    model_import = ModelImportation.objects.get(object_id=base.pk)
    if request.method == 'POST':
        delete_form = DeleteForm(request.POST)
        delete(request, cell, delete_form)
        print(cell)
    return redirect(reverse_lazy('import_data:detail-model-importation', kwargs={'pk': model_import.pk}))
