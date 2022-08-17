from django.urls import path
from .views import *

app_name = 'Ytube'

urlpatterns = [
    path('', index, name='home'),
    path('post/', single, name='single'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('group/', group, name='group'),
    path('group/<slug:post_slug>/', group_posts, name='post'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('support/', support, name='support'),

]