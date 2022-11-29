import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='testuser_1', password='123456qwerty')


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(username='testuser_2', password='123456qwerty')


