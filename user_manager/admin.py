from django.contrib import admin
from .models import *


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'is_active', 'created']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
