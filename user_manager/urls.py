from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
app_name = 'users'

urlpatterns = [
    path('register/', register, name='create_user'),
    path('edit/', edit_user_profile, name='edit_user_profile'),
    path('login/', send_code_by_email, name='send_code_by_email'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy("users:password_change_done")), name='change_password'),
    path('check/code/authentication/', check_authentication_code, name='check_authentication_code'),
    path('logout/', logout_user, name='logout_user')
]
