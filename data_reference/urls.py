from django.urls import include, path
from .views import *
app_name = 'data-reference'
urlpatterns = [
    path('<str:model>/fields/', get_model_fields, name='get_model_fields'),
    path('models/<str:app_label>/', get_all_models, name='get_all_models'),
    path('<str:model>/<str:field_name>/lookups/', get_class_lookups, name='get-class-lookups'),
    path('tables/create-model-table/', create_model_table_view, name='create-model-table'),
    path('tables/all-models-tables/', all_model_tables, name='all-models-tables'),
    path('table/<int:pk>/edit-model-table/', edit_model_table, name='edit-model-table'),
    path('table/<int:pk>/delete-model-table/', delete_model_table, name='delete-model-table'),
    path('table/<int:pk>/detail-model-table/', detail_model_table, name='detail-model-table'),
    path('table/<int:pk>/create-column/', create_column_for_model, name='create-column-for-model'),
    path('table/<int:pk>/delete-column/', delete_column_for_model, name='delete-column-for-model'),
    path('table/<int:pk>/view-table/', view_table_by_model, name='view-table-by-model'),

]