from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Group, Author
from random import randint


def index(request):
    template = 'Ytube/index.html'
    title = 'Funny Blog'
    posts = Post.objects.order_by('created_at')
    count = Post.objects.count()

    random_lst = []
    while len(random_lst) <= 2:
        r = Post.objects.all()[randint(0, count - 1)]
        if r not in random_lst:
            random_lst.append(r)

    paginator = Paginator(Post.objects.all(), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'random_lst': random_lst,
        'title': title,
        'text': 'Главная страница',
        'page_obj': page_obj,
    }
    return render(request, template, context)


def show_post(request, post_slug):
    template = 'Ytube/single.html'
    post = get_object_or_404(Post, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': 1,
    }
    return render(request, template, context)


def group(request):
    template = 'Ytube/group.html'
    title = 'Здесь будет информация о группах проекта Ytube'
    groups = Group.objects.all()[:1]
    context = {
        'groups': groups,
        'title': title,
    }
    return render(request, template, context)


def show_groups(request, post_slug):
    group = get_object_or_404(Group, slug=post_slug)
    posts = Post.objects.filter(group=group).order_by('-created_at')[:7]
    context = {
        'group': group,
        'posts': posts,
        'cat_selected': 1,
    }
    return render(request, 'Ytube/single_group.html', context)



def author(request):
    template = 'Ytube/about.html'
    title = 'Здесь будет информация о группах проекта Ytube'
    authors = Author.objects.all()[:5]
    context = {
        'authors': authors,
        'title': title,
    }
    return render(request, template, context)


def show_authors(request, post_slug):
    return render(request, 'Ytube/about.html')



def single(request):
    return render(request, 'Ytube/single.html')


def contact(request):
    return render(request, 'Ytube/contact.html')
















