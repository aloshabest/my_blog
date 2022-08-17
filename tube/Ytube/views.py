from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    template = 'Ytube/index.html'
    title = 'Funny Blog'
    context = {
        'title': title,
        'text': 'Главная страница',
    }
    return render(request, template, context)


def about(request):
    return render(request, 'Ytube/about.html')


def blog(request):
    template = 'Ytube/blog.html'
    title = 'Здесь будет информация о группах проекта Ytube'
    context = {
        'title': title,
        'text': 'Главная страница',
    }
    return render(request, template, context)


def contact(request):
    return render(request, 'Ytube/contact.html')


def support(request):
    return render(request, 'Ytube/support.html')


def blog_posts_detail(request, pk):
    return HttpResponse(f'Пост номер {pk}')