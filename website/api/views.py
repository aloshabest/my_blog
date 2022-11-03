from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

