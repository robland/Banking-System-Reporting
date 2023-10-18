from django.db import models
from django.contrib.auth.models import User


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to_codes')
    code = models.CharField(max_length=100, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


DEPARTMENT_CHOICES = [
    ('MONETIQUE', 'MONETIQUE'),
    ('OPERATION', 'OPERATION')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=25, default="", null=True)
    image = models.ImageField(upload_to="images/profile/", null=True)
    about = models.TextField(null=True)
    job = models.CharField(max_length=100, default='', null=True)
    address = models.CharField(max_length=100, default='', null=True)
    phone = models.CharField(max_length=100, default="", null=True)

