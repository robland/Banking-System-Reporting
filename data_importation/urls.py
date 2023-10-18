from django.urls import include, path
from rest_framework import routers
from data_importation.views import *


app_name = "importation"

router = routers.DefaultRouter()
router.register(r'importation-viewset', ImportationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('data/', import_data, name='import_data'),
    # path('extraction/<int:pk>/', data_extraction, name='data_extraction'),
    path('extraction/', data_extraction, name='data_extraction'),

    path('create-model/', create_model_importation, name='create-model-importation'),
    path('<int:pk>/detail-model-importation/', detail_model_importation, name='detail-model-importation'),
    path('<int:pk>/delete-model-importation/', delete_model_importation, name='delete-model-importation'),
    path('<int:pk>/edit-model-importation/', edit_model_importation, name='edit-model-importation'),
    path('all-models/', all_models_importation, name='all_models_importation'),
    
    path('<int:pk>/create-regular-expression/', create_regular_expression, name='create-regular-expression'),
    path('<int:pk>/create-regular-expression-for-other-format/',
         create_regular_expression_for_other_format, name='create-regular-expression-for-other-format'),
    path('<int:pk>/detail-regular-expression/', detail_regular_expression, name='detail-regular-expression'),
    path('<int:pk>/delete-regular-expression/', delete_regular_expression, name='delete-regular-expression'),
    path('<int:pk>/edit-regular-expression/', edit_regular_expression, name='edit-regular-expression'),
    
    path('<int:pk>/add-fields-to-cell/', add_field_to_cell, name='add_field_to_cell'),
    path('<int:pk>/add-fields-to-regular-expression/',
         add_field_to_regular_expression, name='add-fields-to-regular-expression'),
    path('<int:pk>/detail-fields-to-cell/', detail_field_to_cell, name='detail-field-to-cell'),
    path('<int:pk>/delete-fields-to-cell/', delete_field_to_cell, name='delete-field-to-cell'),
    path('<int:pk>/edit-fields-to-cell/', edit_field_to_cell, name='edit-field-to-cell'),

    path('<int:pk>/delete-cell/', delete_base_cell, name='delete-base-cell'),
    
]