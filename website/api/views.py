from blog.models import Post, Group, Author, Comment
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import PostSerializer, GroupSerializer, AuthorSerializer, CommentSerializer
from rest_framework import viewsets
from .permissions import IsAuthorOrReadOnly
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication, BasicAuthentication)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication, BasicAuthentication)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication, BasicAuthentication)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication, BasicAuthentication)

    def get_queryset(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id')).comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user)

