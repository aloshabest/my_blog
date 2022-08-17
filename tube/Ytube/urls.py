from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('about/', about),
    path('blog/', blog),
    path('contact/', contact),
    path('support/', support),
    path(
        'blog/<int:pk>/',
        blog_posts_detail
    ),
]