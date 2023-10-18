from django import forms
from django.contrib.auth.models import User
from .models import Profile, DEPARTMENT_CHOICES


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    otp_code = forms.CharField(max_length=100, required=False)


class UserEditForm(forms.ModelForm):
    # password = forms.CharField()
    # password2 = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    """def clean_password(self):
        cd = self.cleaned_data

        if cd['password'] != cd["password2"]:
            raise forms.ValidationError("les mots de passe fournis sont différents.")
        return cd['password2']"""


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            'department': forms.Select(choices=DEPARTMENT_CHOICES)
        }

