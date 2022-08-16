from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('group/', group_posts),
    path(
        'group/<int:pk>/',
        group_posts_detail
    ),
]