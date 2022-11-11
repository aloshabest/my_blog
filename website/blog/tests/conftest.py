import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ConfTest(TestCase):
    @pytest.mark.django_db
    def test_register_success(self):
        superuser = User.objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="admin"
        )
        superuser.save()
        assert User.objects.count() > 0, (
            'Не был создан superuser'
        )

    @pytest.mark.django_db
    def create_test_user(self):
        test_user = User.objects.create(
            firstname='testtesttest',
            lastsname='testtesttest',
            username="test_user",
            email="test_user@test_user.com",
            password="test_user"
        )
        test_user.save()
        return test_user

