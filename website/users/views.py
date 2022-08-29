from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .form import CreationForm, ContactForm, ProfileForm
from django.contrib.auth.models import User


def password_reset_form(request):
    return render(request, 'blog/index.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class UserContact(CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('blog:home')
    template_name = 'users/contact.html'


class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('blog:home')
    template_name = 'users/profile.html'






