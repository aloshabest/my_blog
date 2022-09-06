from django import template
from blog.models import Post, Author, Group
import random
from django.db.models import Count


register = template.Library()

@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}


@register.inclusion_tag('blog/author_bio_tpl.html')
def get_bio():
    authors = random.choice(Author.objects.all())
    return {'authors': authors}


@register.inclusion_tag('blog/categories_tpl.html')
def get_categories():
    categories = Group.objects.all()
    res = [(c, Post.objects.filter(group=c).count()) for c in categories]
    return {'res': res}