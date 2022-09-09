from django.urls import path, include
from .views import *
from django.conf import settings
import debug_toolbar
from django.conf.urls.static import static


app_name = 'blog'

urlpatterns = [
    path('', index, name='home'),
    path('post/new/', post_new, name='post_new'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:post_slug>/edit/', post_edit, name='post_edit'),
    path('group/<slug:post_slug>/', show_groups, name='groups'),
    path('authors/', authors, name='authors'),
    path('author/<slug:post_slug>/', show_authors, name='author'),
    path('author/<str:username>/follow/', get_follow, name='get_follow'),
    path('author/<str:username>/unfollow/', get_unfollow, name='get_unfollow'),
    path('my_posts/', my_posts, name='my_posts'),
    path('search/', Search.as_view(), name='search'),
    path('subscriptions/', subscriptions, name='subscriptions'),


]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)