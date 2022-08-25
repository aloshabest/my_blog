from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .form import CreationForm


def password_reset_form(request):
    return render(request, 'Ytube/index.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('Ytube:home')
    template_name = 'users/signup.html'


