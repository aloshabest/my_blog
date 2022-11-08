import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    user = User.objects.create_user(username='elonmask', email='e@m.ru', password='123456fktrctq')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {refresh.access_token}')

    return client

@pytest.fixture
def group_1():
    from blog.models import Group
    return Group.objects.create(title='Группа 1', slug='test_test_4', description='testing')


@pytest.fixture
def group_2():
    from blog.models import Group
    return Group.objects.create(title='Группа 2', slug='test_test_3', description='testing')


@pytest.fixture
def post(user, group_1):
    from blog.models import Post
    return Post.objects.create(title='Тестовый пост 1', content='testing', slug='test_test_1', author=user, group=group_1, photo='photo/2022/11/03/07-4.jpg')


@pytest.fixture
def post_2(user, group_1):
    from blog.models import Post
    return Post.objects.create(title='Тестовый пост 12342341', content='testing', slug='test_test_2', author=user, group=group_1, photo='photo/2022/11/03/07-4.jpg')


@pytest.fixture
def comment_1_post(post, user):
    from blog.models import Comment
    return Comment.objects.create(author=user, post=post, content='Коммент 1', photo='photo/2022/08/29/Bill_Gates_2017_cropped.jpg')


@pytest.fixture
def comment_2_post(post, another_user):
    from blog.models import Comment
    return Comment.objects.create(author=another_user, post=post, content='Коммент 2', photo='photo/2022/08/29/Bill_Gates_2017_cropped.jpg')


@pytest.fixture
def another_post(another_user, group_2):
    from blog.models import Post
    return Post.objects.create(title='Тестовый пост 2', content='testing', author=another_user, group=group_2, photo='photo/2022/11/03/07-4.jpg')


@pytest.fixture
def comment_1_another_post(another_post, user):
    from blog.models import Comment
    return Comment.objects.create(author=user, post=another_post, content='Коммент 12', photo='photo/2022/08/29/Bill_Gates_2017_cropped.jpg')


