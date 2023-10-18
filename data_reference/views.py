from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework.renderers import JSONRenderer
from django.db import models
from django.contrib.contenttypes.models import ContentType

from data_importation.views import delete
from data_reference.forms import *
from data_importation.forms import DeleteForm


def get_fields_for_model(model):
    model = ContentType.objects.get(model__icontains=model)
    fields = [[v.name, str([t.name for t in v.related_model._meta.fields]) if v.is_relation else False] for i, v in
              enumerate(model.model_class()._meta.fields)]
    return fields


def get_model_fields(request, model, app_label=None):
    fields = get_fields_for_model(model)
    # serial = JSONRenderer().render(fields)
    return JsonResponse(fields, safe=False, status=200)


def get_class_lookups(request, model, field_name):
    model = ContentType.objects.get(model__contains=model)
    fields = model.model_class()._meta.fields
    lookups = []
    for field in fields:
        temp = field.get_lookups().keys() if field.attname == field_name else None
        if temp is not None:
            lookups = list(temp)

    return JsonResponse(lookups, safe=False, status=200)


def get_all_models(request, app_label):
    tables = ContentType.objects.filter(app_label__icontains=app_label)
    tables = [i.model for i in tables]
    return JsonResponse(tables, safe=False, status=200)


def get_model_filter_kwargs(request, fields):
    pass


def create_model_table_view(request):
    form = ModelTableForm()

    if request.method == "POST":
        form = ModelTableForm(request.POST)

        if form.is_valid():
            form.save()

            if form.cleaned_data['next_action'] == "1":
                return redirect(reverse_lazy("data-reference:create-model-table"))
            elif form.cleaned_data["next_action"] == "2":
                return HttpResponse("Ajouter des colonnes à ce modèle")
            return HttpResponse("Form Validated!")
        else:
            return render(request, 'data_reference/create-model-table-view.html', locals())

    return render(request, 'data_reference/create-model-table-view.html', locals())


def all_model_tables(request):
    all_tables = ModelTable.objects.all()
    return render(request, 'data_reference/all_models_tables.html', locals())


def edit_model_table(request, pk):
    model_table = get_object_or_404(ModelTable, pk=pk)
    form = ModelTableForm(instance=model_table)
    if request.method == "POST":
        form = ModelTableForm(request.POST)
        if form.is_valid():
            # form.save()
            ModelTable.objects.filter(pk=pk).update(**{key:value for key, value in form.cleaned_data.items()
                                                       if key != "next_action"})

            if form.cleaned_data['next_action'] == "1":
                return redirect(reverse_lazy("data-reference:create-model-table"))
            elif form.cleaned_data["next_action"] == "2":
                return HttpResponse("Ajouter des colonnes à ce modèle")
            return redirect(reverse_lazy('data-reference:all-models-tables'))
        else:
            return render(request, 'data_reference/create-model-table-view.html', locals())

    return render(request, 'data_reference/create-model-table-view.html', locals())


def delete_model_table(request, pk):
    model_table = get_object_or_404(ModelTable, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        delete(request, model_table, form)
    return redirect(reverse_lazy("data-reference:all-models-tables"))


def detail_model_table(request, pk):
    model_table = get_object_or_404(ModelTable, pk=pk)
    return render(request, 'data_reference/detail-model-table.html', locals())


def create_column_for_model(request, pk):
    model_table = get_object_or_404(ModelTable, pk=pk)
    fields = get_fields_for_model(model_table.model_name)
    form = ModelColumnForm()

    if request.method == 'POST':
        form = ModelColumnForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.model_table = model_table
            instance.save()

            if form.cleaned_data['next_action'] == "1":
                return redirect(reverse_lazy("data-reference:create-column-for-model", kwargs={'pk': model_table.pk}))
            elif form.cleaned_data["next_action"] == "2":
                return HttpResponse("Ajouter des colonnes à ce modèle")

            return redirect(reverse_lazy("data-reference:detail-model-table", kwargs={'pk': model_table.pk}))
        else:
            return render(request, 'data_reference/create-column-for-table.html', locals())
    return render(request, 'data_reference/create-column-for-table.html', locals())


def delete_column_for_model(request, pk):
    column = get_object_or_404(ModelColumn, pk=pk)
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        delete(request, column, form)
    return redirect(reverse_lazy("data-reference:detail-model-table", kwargs={'pk': column.model_table.pk}))


def edit_column_for_model(request, pk):
    pass


def view_table_by_model(request, pk):
    model_table = get_object_or_404(ModelTable, pk=pk)
    model = ContentType.objects.get(model=model_table.model_name)
    headers = [i.name for i in model_table.table_to_fields.all()]
    data = [[getattr(obj, i) for i in headers if hasattr(obj, i)] for obj in model.model_class().objects.all()]
    try:
        headers = headers[:len(data[0]) if len(headers) > len(data[0]) else len(headers)]
    except IndexError as e:
        pass

    return render(request, 'data_reference/view-table-by-model.html', locals())
