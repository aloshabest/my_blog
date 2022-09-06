from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from .models import Post, Group, Author, Comment
from random import randint, choice
from .forms import PostForm, CommentForm
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.text import slugify
from django.db.models import F


def index(request):
    template = 'blog/index.html'
    title = 'Funny Blog'

    # Показ постов и количества комментариев каждого поста
    res = [(p, Comment.objects.filter(post=p).count()) for p in Post.objects.order_by('created_at')]

    # Показ 3-х случайных постов и количества комментариев каждого поста
    random_lst = []
    while len(random_lst) <= 2:
        r = Post.objects.all()[randint(0, Post.objects.count() - 1)]
        if r not in random_lst:
            random_lst.append(r)
    random_res = [(r, Comment.objects.filter(post=r).count()) for r in random_lst]

    # Пагинация
    paginator = Paginator(tuple((p, Comment.objects.filter(post=p).count()) for p in Post.objects.all()), 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'random_lst': random_lst,
        'title': title,
        'text': 'Главная страница',
        'page_obj': page_obj,
        'res': res,
        'random_res': random_res,
    }
    return render(request, template, context)


def show_post(request, post_slug):
    template = 'blog/single.html'
    post = get_object_or_404(Post, slug=post_slug)

    created_by = get_object_or_404(Author, title=post.author)

    comments = post.comments.filter(active=True)

    post.views = F('views') + 1
    post.save()
    post.refresh_from_db()

    if request.method == "POST":
        author = get_object_or_404(Author, user_id=request.user.id)
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)

                if parent_obj:
                    replay_comment = form.save(commit=False)
                    replay_comment.parent = parent_obj
                    replay_comment.reply_to = parent_obj.author

            comment = form.save(commit=False)
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
        'created_by': created_by,
    })


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


def sidebar(request):
    template = 'includes/sidebar.html'
    authors = Author.objects.all()
    rand_author = choice(authors)


    context = {
        'authors': authors,
        'rand_author': rand_author
    }
    return render(request, template, context)


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context











