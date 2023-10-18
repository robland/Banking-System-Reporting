from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from rest_framework.parsers import JSONParser
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.response import Response
# from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .forms import *

from .serializers import RegisterUserSerializer,  MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny

import string
import random

from django.core.mail import send_mail
from .models import OTP


def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@login_required
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            code = ''
            for i in range(4):
                code += '-' + get_random_string(6)
            new_user.set_password(
                code
            )
            try:
                sent = send_mail(
                    "Credentials informations",
                    f"your password: {code}\n Your username: {new_user.username}",
                    "okoleonrobland@gmail.com",
                    [new_user.email]
                )
                new_user.save()
            except:
                # return JsonResponse({'error': True, 'detail': 'Bad SMTP Configuration'}, status=403)
                user_form.add_error('email', "Bad SMTP Configuration")
                return render(request, 'registration/login.html', {'errors': user_form.errors, 'user_form': user_form})

            return render(request, 'registration/register_done.html', {'new_user': new_user})
        return render(request, 'registration/register.html', {'errors': user_form.errors, 'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            code = ''
            for i in range(4):
                code += '-' + get_random_string(6)
            new_user.set_password(
                code
            )
            try:
                sent = send_mail(
                    "Credentials informations",
                    f"your password: {code}\n Your username: {new_user.username}",
                    "okoleonrobland@gmail.com",
                    [new_user.email]
                )
                new_user.save()
                Profile.objects.create(user=new_user)
            except:
                # return JsonResponse({'error': True, 'detail': 'Bad SMTP Configuration'}, status=403)
                user_form.add_error('email', "Bad SMTP Configuration")
                return render(request, 'registration/login.html', {'errors': user_form.errors, 'user_form': user_form})

            return render(request, 'registration/register_done.html', {'new_user': new_user})
        return render(request, 'registration/register.html', {'errors': user_form.errors, 'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('users:send_code_by_email'))


@login_required
def edit_user_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/edit.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'profile': request.user.profile, 'departments': DEPARTMENT_CHOICES}
                  )


class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            if new_user:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'registration/login.html', {})


@csrf_exempt
def send_code_by_email(request):
    form = LoginForm()
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        # serial_user = UserOTPSerializer(data=data)
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                code = 'BSR'
                while True:
                    for i in range(4):
                        code += '-' + get_random_string(6)

                    otp, created = OTP.objects.get_or_create(code=code, user=user)
                    if created:
                        break
                    else:
                        code = 'BSR'
                try:
                    sent = send_mail(
                        "This is your otp code}",
                        f"otp code: {otp.code}",
                        "okoleonrobland@gmail.com",
                        [user.email]
                    )
                    data = {
                        'sent': sent,
                        'user': user.id
                    }
                    print()
                    # return JsonResponse(data, status=201)
                    return render(request, 'registration/login_final_step.html', {'form': form})
                except Exception as e:
                    # return JsonResponse({'error': True, 'detail': 'Bad SMTP Configuration'}, status=403)
                    print(e)
                    form.add_error('otp_code', "Bad 1 SMTP Configuration")
                    return render(request, 'registration/login.html', {'errors': form.errors, 'form': form})
            # return JsonResponse({'error': True, 'detail': "Incorrect username and password"}, status=403)
            form.add_error('username', "Incorrect Username and Password")
            return render(request, 'registration/login.html', {'errors': form.errors, "form": form})
        # return JsonResponse({'error': True, 'detail':  serial_user.errors}, status=403)
        return render(request, 'registration/login.html', {'errors': form.errors, 'form': form})
    else:
        return render(request, 'registration/login.html', locals())


@csrf_exempt
def check_authentication_code(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Get user here
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("I'm Here!")

                try:
                    print(user.user_to_codes.last().code, form.cleaned_data['otp_code'])
                    otp = user.user_to_codes.filter(is_active=True).last()
                    if otp.code == form.cleaned_data['otp_code']:
                        otp.is_active = False
                        otp.save()
                        login(request, user)
                        # return JsonResponse({'success': True}, status=201)
                        return render(request, 'test.html', {})
                except:
                    form.add_error('otp_code', "Bad Authentication code was provided")
            return render(request, 'registration/login_final_step.html', {'errors': form.errors, 'form': form})
    return redirect('users:send_code_by_email')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
