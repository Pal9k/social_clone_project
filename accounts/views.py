from django.shortcuts import render
# if someone logged in or logedout where they should go
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms
# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateFrom
    # if someone successfully signedUp the success_url will take them to the login page
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
