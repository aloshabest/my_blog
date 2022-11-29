from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import CommentViewSet, GroupViewSet, PostViewSet, AuthorViewSet


router = SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet)


urlpatterns = [
    # path('v1/drf-auth/', include('rest_framework.urls')),
    # path('v1/auth/', include('djoser.urls')),
    path('v1/', include(router.urls)),
]
