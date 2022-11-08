from rest_framework.serializers import ModelSerializer, SlugRelatedField, CurrentUserDefault
from blog.models import Post, Group, Author, Comment


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

