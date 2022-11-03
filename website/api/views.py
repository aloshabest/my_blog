from blog.models import Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import PostSerializer
from rest_framework import viewsets
from .permissions import IsAuthorOrReadOnly
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (IsAuthorOrReadOnly,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication, BasicAuthentication)



