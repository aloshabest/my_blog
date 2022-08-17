from django.urls import path
from .views import *

app_name = 'Ytube'

urlpatterns = [
    path('', index, name='home'),
    path('post/', single, name='single'),
    path('about/', about, name='about'),
    path('group/', group, name='group'),
    path('contact/', contact, name='contact'),
    path('support/', support, name='support'),
    path('group/<slug>/', group_posts_1, name='group_posts_1'),
]