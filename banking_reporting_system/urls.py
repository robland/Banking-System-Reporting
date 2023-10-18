from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from data_reporting.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_manager.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('snippets.urls')),
    path('accounts/', include('user_manager.urls', namespace='users')),
    path('api/importation/', include('data_importation.urls', namespace='import_data')),
    path('api/data-reporting/', include('data_reporting.urls', namespace='data_reporting')),
    path('api/data-reference/', include('data_reference.urls')),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
