import pytest
from blog.models import Group, Post, Comment

@pytest.fixture
def group_1():
    return Group.objects.create(title='Группа 1', slug='test_test_4', description='testing')


@pytest.fixture
def group_2():
    return Group.objects.create(title='Группа 2', slug='test_test_3', description='testing')


@pytest.fixture
def post(user, group_1):
    return Post.objects.create(title='Тестовый пост 1', content='testing', slug='test_test_1', author=user, group=group_1, photo='photo/2022/11/03/07-4.jpg')


@pytest.fixture
def post_2(user, group_1):
    return Post.objects.create(title='Тестовый пост 12342341', content='testing', slug='test_test_2', author=user, group=group_1, photo='photo/2022/11/03/07-4.jpg', views=5)


@pytest.fixture
def comment_1_post(post, user):
    return Comment.objects.create(author=user, post=post, content='Коммент 1', photo='photo/2022/08/29/Bill_Gates_2017_cropped.jpg')


@pytest.fixture
def comment_2_post(post, another_user):
    return Comment.objects.create(author=another_user, post=post, content='Коммент 2', photo='photo/2022/08/29/Bill_Gates_2017_cropped.jpg')
