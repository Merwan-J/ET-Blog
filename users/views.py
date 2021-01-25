from django.shortcuts import render
from django.views.generic import FormView
from .forms import SignUpForm
from django.urls import reverse_lazy
# Create your views here.

class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')