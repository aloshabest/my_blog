from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'Ytube/index.html')


def about(request):
    return render(request, 'Ytube/about.html')


def blog(request):
    return render(request, 'Ytube/blog.html')


def contact(request):
    return render(request, 'Ytube/contact.html')


def support(request):
    return render(request, 'Ytube/support.html')


def group_posts(request):
    return HttpResponse('Посты, отфильтрованные по группам')


def group_posts_detail(request, pk):
    return HttpResponse(f'Пост номер {pk}')