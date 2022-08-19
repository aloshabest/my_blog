from django.urls import path, include
from .views import *
from django.conf import settings
import debug_toolbar
from django.conf.urls.static import static


app_name = 'Ytube'

urlpatterns = [
    path('', index, name='home'),
    path('post/', single, name='single'),
    path('post/<slug:slug>/', show_post, name='post'),
    path('group/', group, name='group'),
    path('group/<slug:slug>/', group_posts, name='groups'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)