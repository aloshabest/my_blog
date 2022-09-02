from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Group, Author, Comment
from random import randint
from .forms import PostForm, CommentForm
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.text import slugify



def index(request):
    template = 'blog/index.html'
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


def show_post(request, post_slug, parent_id=None):
    template = 'blog/single.html'
    post = get_object_or_404(Post, slug=post_slug)

    comments = post.comments.filter(active=True)

    if request.method == "POST":
        author = get_object_or_404(Author, user_id=request.user.id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))

            comment.post = post
            comment.author = request.user
            comment.photo = author.photo


            comment.save()
            return redirect(post.get_absolute_url())
    else:

        form = CommentForm()

    return render(request, template, {
        'post': post,
        'title': post.title,
        'comments': comments,
        'form': form,
        'parent_id': parent_id,
    })


def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  # from hidden input
            parent_id = request.POST.get('parent')  # from hidden input
            post_url = request.POST.get('post_url')  # from hidden input
            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url + '#' + str(reply.id))
    return redirect("/")


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
    return render(request, 'blog/single_group.html', context)


def authors(request):
    template = 'blog/authors.html'
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
    template = 'blog/about.html'
    author = get_object_or_404(Author, slug=post_slug)
    posts = Post.objects.filter(author=author.user).order_by('-created_at')

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author': author,
        'cat_selected': 1,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def my_posts(request):
    template = 'blog/my_posts.html'
    author = get_object_or_404(Author, user=request.user)
    posts = Post.objects.filter(author=author.user).order_by('-created_at')

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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def post_edit(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    is_edit = True
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(str(post))
            post.is_edit = is_edit
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
            'is_edit': is_edit,
        }
    return render(request, 'blog/create_post.html', context)


# def add_comment(request, post_slug, parent_comment_id=None):
#     if request.method == "POST":
#         post = get_object_or_404(Post, slug=post_slug, user=request.user)
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.user = request.user
#             if parent_comment_id:
#                 parent_comment = Comment.objects.get(id=parent_comment_id)
#                 comment.parent_id = parent_comment.get_root().id
#                 comment.reply_to = parent_comment.user
#                 comment.save()
#
#                 return HttpResponse('200 OK')
#
#             comment.save()
#             return HttpResponseRedirect(post.get_absolute_url())
#     else:
#         form = CommentForm()
#         context = {
#             'form': form,
#             'post_slug': post_slug,
#             'parent_comment_id': parent_comment_id,
#         }
#     return render(request, 'blog/single.html', context)














