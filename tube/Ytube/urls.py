from django.urls import path, include
from .views import *
from django.conf import settings
import debug_toolbar
from django.conf.urls.static import static


app_name = 'Ytube'

urlpatterns = [
    path('', index, name='home'),
    path('post/', single, name='single'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('group/', group, name='group'),
    path('group/<slug:post_slug>/', show_groups, name='groups'),
    path('author/', author, name='author'),
    path('author/<slug:post_slug>/', show_authors, name='authors'),
    path('contact/', contact, name='contact'),

]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)