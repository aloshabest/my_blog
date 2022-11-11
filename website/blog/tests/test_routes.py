import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Post, Group, Follow, Author, Comment
from django.urls import reverse


class RouteTest(TestCase):
    @pytest.mark.django_db
    def test_index(self):
        homepage_url = reverse("blog:home")
        response = self.client.get(homepage_url)
        assert response.status_code == 200
        assert response.context["request"].path == "/"

