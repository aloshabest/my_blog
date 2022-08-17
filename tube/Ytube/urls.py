from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('about/', about),
    path('blog/', blog),
    path('contact/', contact),
    path('support/', support),
    path('group/', group_posts),
    path(
        'group/<int:pk>/',
        group_posts_detail
    ),
]