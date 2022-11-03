from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView


@authentication_classes(())
@permission_classes(())
class PostAPIList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



