from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Group, Author
from random import randint
from .forms import PostForm
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from time import timezone
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


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


def show_groups(request, post_slug):
    group = get_object_or_404(Group, slug=post_slug)
    posts = Post.objects.filter(group=group).order_by('-created_at')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'posts': posts,
        'cat_selected': 1,
        'page_obj': page_obj,
    }
    return render(request, 'Ytube/single_group.html', context)



def authors(request):
    template = 'Ytube/authors.html'
    authors = Author.objects.all()

    paginator = Paginator(authors, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'authors': authors,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def show_authors(request, post_slug):
    template = 'Ytube/about.html'
    author = get_object_or_404(Author, slug=post_slug)
    posts = Post.objects.filter(author=author).order_by('-created_at')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'cat_selected': 1,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = Author.objects.get(user=request.user)
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'Ytube/post_form.html', {'form': form})






# def post_create(request):
#     template = 'Ytube/create_post.html'
#     form = PostForm
#     return render(request, template, context={'form': form})


# class PostCreate(CreateView):
#     form_class = PostForm
#     success_url = reverse_lazy('Ytube:home')
#     template_name = 'Ytube/create_post.html'













