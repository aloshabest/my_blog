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
    path('group/<slug:post_slug>/', show_groups, name='groups'),
    path('authors/', authors, name='authors'),
    path('author/<slug:post_slug>/', show_authors, name='author'),


]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)