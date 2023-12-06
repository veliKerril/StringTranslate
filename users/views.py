from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegistrationUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('main-page')


class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'users/registration.html'
    extra_context = {'title': 'Регистрация'}

    def get_success_url(self):
        return reverse_lazy('main-page')
