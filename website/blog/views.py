from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from .models import Post, Group, Author, Comment, Follow
from random import randint, choice, sample
from .forms import PostForm, CommentForm
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.text import slugify
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views import View


User = get_user_model()


class Index(View):

    def get(self, request, *args, **kwargs):
        template = 'blog/index.html'
        title = 'Funny Blog'

        # Показ постов и количества комментариев каждого поста
        posts = [(p, Comment.objects.filter(post=p).count()) for p in Post.objects.order_by('created_at')]

        # Показ 3-х случайных постов и количества комментариев каждого поста
        random_posts = [(r, Comment.objects.filter(post=r).count()) for r in sample(list(Post.objects.all()), min(3, len(list(Post.objects.all()))))]

        # Пагинация
        paginator = Paginator(tuple((p, Comment.objects.filter(post=p).count()) for p in Post.objects.all()), 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'posts': posts,
            'random_posts': random_posts,
        }
        return render(request, template, context)


class ShowPost(View):

    def get(self, request, slug, *args, **kwargs):
        template = 'blog/single.html'
        post = get_object_or_404(Post, slug=slug)

        created_by = get_object_or_404(Author, title=post.author)

        comments = post.comments.filter(active=True)

        post.views = F('views') + 1
        post.save()
        post.refresh_from_db()

        form = CommentForm()

        return render(request, template, {
            'post': post,
            'title': post.title,
            'comments': comments,
            'form': form,
            'created_by': created_by,
        })

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        author = get_object_or_404(Author, user_id=request.user.id)
        form = CommentForm(request.POST)
        if form.is_valid():
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


class ShowCategories(View):

    def get(self, request, slug, *args, **kwargs):
        group = get_object_or_404(Group, slug=slug)
        posts = Post.objects.filter(group=group).order_by('-created_at')

        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'group': group,
            'posts': posts,
            'page_obj': page_obj,
        }
        return render(request, 'blog/single_group.html', context)


class Authors(ListView):
    model = Author
    template_name = 'blog/authors.html'
    context_object_name = 'authors'
    paginate_by = 5

    def get_queryset(self):
        return Author.objects.filter(number_of_posts__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SingleAuthor(ListView):
    template_name = 'blog/about.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        self.author = get_object_or_404(Author, slug=self.kwargs['slug'])
        return [(r, Comment.objects.filter(post=r).count()) for r in Post.objects.filter(author=self.author.user)]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = Author.objects.get(slug=self.kwargs['slug'])
        context['count'] = Post.objects.filter(author=self.author.user).count()
        return context


class NewPost(View):
    def get(selfself, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'blog/create_post.html', {'form': form})

    def post(self, request, *args, **kwargs):

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post)
            post.author = request.user
            post.save()

            request.user.number_of_posts = F('number_of_posts') + 1
            request.user.save()
            request.user.refresh_from_db()

            return HttpResponseRedirect(post.get_absolute_url())
        else:
            return render(request, 'blog/create_post.html', {'form': form})

class EditPost(View):
    def get(selfself, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        is_edit = True
        form = PostForm(instance=post)
        context = {
            'form': form,
            'is_edit': is_edit,
        }

        return render(request, 'blog/create_post.html', context)

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(str(post))
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            return render(request, 'blog/create_post.html', {'form': form})

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


class Subscriptions(View):

    def get(self, request, *args, **kwargs):
        template = 'blog/subscriptions.html'

        user = request.user
        authors = user.follower.values_list('author', flat=True)
        author = Author.objects.filter(user__id__in=authors)

        paginator = Paginator(tuple((p, Comment.objects.filter(post=p).count()) for p in Post.objects.filter(author__id__in=authors).order_by('created_at')), 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'author': author,
            'page_obj': page_obj,
        }
        return render(request, template, context)


@login_required
def get_follow(request, username):
    author = User.objects.get(username=username)
    user = request.user

    if author != user:
        Follow.objects.get_or_create(user=user, author=author)
        return redirect('blog:subscriptions')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def get_unfollow(request, username):
    user = request.user
    Follow.objects.get(user=user, author__username=username).delete()
    return redirect('blog:subscriptions')







