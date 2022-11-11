import pytest
from blog.models import Post, Group, Follow, Author, Comment
from django.contrib.auth.models import User
from conftest import ConfTest
from django.test import TestCase


class ModelTest(TestCase):
    @pytest.mark.django_db
    def test_category_model_persists(self):
        new_category = Group()
        new_category.title = "new_category"
        new_category.slug = "test_category"
        new_category.save()
        assert new_category.title == "new_category", (
            'Не было задано название категории'
        )

        assert Group.objects.count() > 0, (
            'Категория не была занесена в базу данных'
        )

    @pytest.mark.django_db
    def test_post_model_persists(self):
        new_post = Post()
        new_post.title = "new_post"
        new_post.author = ConfTest.create_test_user(self)
        old_post_obj_count = Post.objects.filter().count()
        new_post.slug = "test_post_slug"
        new_post.photo = "photo/2022/11/03/07-4.jpg"
        new_post.group = 1
        new_post.save()
        new_post_obj_count = Post.objects.filter().count()
        assert new_post.title == "new_post", (
            'Не было задано название поста'
        )

        assert old_post_obj_count < new_post_obj_count, (
            'Пост не был занесен в базу данных'
        )

    @pytest.mark.django_db
    def test_comment_model_persists(self):
        new_comment = Comment()
        new_comment.post = 49
        new_comment.author = 25
        new_comment.content = "test"
        new_comment.photo = "photo/2022/11/03/07-4.jpg"
        new_comment.save()
        assert new_comment.post == 49, (
            'Не было задано пост, к которому комментарий'
        )

        assert Comment.objects.count() > 0, (
            'Комментарий не был занесена в базу данных'
        )

    @pytest.mark.django_db
    def test_comment_model_persists(self):
        new_author = Author()
        new_author.title = "test_author"
        new_author.slug = "test_author_slug"
        new_author.user = ConfTest.create_test_user(self)
        new_author.photo = "photo/2022/11/03/07-4.jpg"
        new_author.save()
        assert new_author.title == "test_author", (
            'Не было задан автор'
        )

        assert Author.objects.count() > 0, (
            'Автор не был занесен в базу данных'
        )

    @pytest.mark.django_db
    def test_comment_model_persists(self):
        new_follow = Follow()
        new_follow.user = ConfTest.create_test_user(self)
        new_follow.author = 25
        new_follow.save()
        assert new_follow.author == 25, (
            'Не было задано автор, на которого подписываются'
        )

        assert Follow.objects.count() > 0, (
            'ПОдписка не была занесена в базу данных'
        )