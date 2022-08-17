from django.urls import path
from .views import *

app_name = 'Ytube'

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
    path('support/', support, name='support'),
    path(
        'blog/<int:pk>/',
        blog_posts_detail
    ),
]