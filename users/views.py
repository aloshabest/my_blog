from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import CreationForm, ContactForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction


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


@login_required
@transaction.atomic
def update_profile(request, post_slug):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.author)
        if profile_form.is_valid():
            post = profile_form.save(commit=False)
            post.save()
            return redirect('blog:home')

    else:
        profile_form = ProfileForm(instance=request.user.author)
    return render(request, 'users/profile.html', {
        'profile_form': profile_form
    })





