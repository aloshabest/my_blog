from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Group
from django.views.generic import ListView, DetailView
from django.db.models import F


def index(request):
    template = 'Ytube/index.html'
    title = 'Funny Blog'
    posts = Post.objects.order_by('created_at')[:2]
    context = {
        'posts': posts,
        'title': title,
        'text': 'Главная страница',
    }
    return render(request, template, context)


def group(request):
    template = 'Ytube/group.html'
    title = 'Здесь будет информация о группах проекта Ytube'
    groups = Group.objects.all()
    context = {
        'groups': groups,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'Ytube/single.html'
    groups = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-created_at')[:10]
    context = {
        'groups': groups,
        'posts': posts,
    }
    return render(request, template, context)


def group_posts_1(request, slug):
    template = 'Ytube/single.html'
    title = 'Funny Blog'
    posts = Post.objects.get(slug=slug)
    context = {
        'posts': posts,
        'title': title,
        'text': 'Главная страница',
    }
    return render(request, template, context)


def about(request):
    return render(request, 'Ytube/about.html')


def single(request):
    return render(request, 'Ytube/single.html')


def contact(request):
    return render(request, 'Ytube/contact.html')


def support(request):
    return render(request, 'Ytube/support.html')








