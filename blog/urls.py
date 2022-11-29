from django.urls import path, include
from .views import *
from django.conf import settings
import debug_toolbar
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page


app_name = 'blog'

urlpatterns = [
    path('', cache_page(6 * 3)(Index.as_view()), name='home'),
    path('post/new/', NewPost.as_view(), name='post_new'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('post/<slug:slug>/edit/', EditPost.as_view(), name='post_edit'),
    path('category/<slug:slug>/', ShowCategories.as_view(), name='groups'),
    path('authors/', Authors.as_view(), name='authors'),
    path('author/<slug:slug>/', SingleAuthor.as_view(), name='author'),
    path('author/<str:username>/follow/', get_follow, name='get_follow'),
    path('author/<str:username>/unfollow/', get_unfollow, name='get_unfollow'),
    path('search/', Search.as_view(), name='search'),
    path('subscriptions/', Subscriptions.as_view(), name='subscriptions'),


]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)