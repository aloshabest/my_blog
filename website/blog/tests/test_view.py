import pytest
from blog.models import Group, Post, Comment, Follow, Author
from django.urls import reverse


class TestPost:

    @pytest.mark.django_db(transaction=True)
    def test_index(self, client):
        response = client.get('')
        assert response.status_code != 404, (
            'Страница `` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_show_post(self, client, post):
        old_views = post.views
        response = client.get(f'post/{post.slug}/')
        new_views = post.views

        assert new_views > old_views, (
            'Не обновляется счетчкик посмотров поста'
        )

        assert response.status_code == 200, (
            f'Страница `post/{post.slug}/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_show_categories(self, client, post):
        response = client.get(f'/category/{post.group.slug}/')

        assert response.status_code == 200, (
            f'Страница `/category/{post.group.slug}/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_authors(self, client, post):
        response = client.get('/authors/')

        assert response.status_code == 200, (
            'Страница `/authors/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_single_authors(self, client, user):
        response = client.get(f'/author/{user.username}/')

        assert response.status_code == 200, (
            f'Страница `/author/{user.username}/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_new_post(self, client, user):
        client.post('/auth/login/', {'username': 'testuser_1', 'password': '123456qwerty'})
        post_count = Post.objects.count()

        data = {'title': 'Статья номер 3', 'photo': 'photo/2022/11/03/07-4.jpg', 'group': 1}
        response = client.post('/post/new/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/post/new/` с правильными данными возвращается статус 201'
        )

        assert post_count + 1 == Post.objects.count(), (
            'Проверьте, что при POST запросе на `/post/new/` создается статья'
        )

    @pytest.mark.django_db(transaction=True)
    def test_edit(self, client, user, post):
        client.post('/auth/login/', {'username': 'testuser_1', 'password': '123456qwerty'})
        post_count = Post.objects.count()

        data = {'title': 'Статья номер 3_edit'}
        response = client.post(f'/post/{post.slug}/edit/', data=data)
        assert response.status_code == 302
        assert response['Location'] == reverse('blog:post'), (
            f'Проверьте, что при POST запросе на `/post/{post.slug}/edit/` с правильными данными идет перенаправление на страницу поста'
        )

        assert post_count == Post.objects.count(), (
           f'Проверьте, что при POST запросе на `/post/{post.slug}/edit/` не создается новая статья, а меняется текущая'
        )

    @pytest.mark.django_db(transaction=True)
    def test_search(self, client):
        data = ['letter', 'пост', 'author']
        for item in data:
            response = client.get(f'/search/?s={item}/')

            assert response.status_code == 200, (
                f'Страница `/search/?s={item}` не найдена, проверьте этот адрес в *urls.py*'
            )

    @pytest.mark.django_db(transaction=True)
    def test_subscriptions(self, client, user, user_2):
        count = Follow.objects.count()

        client.post('/auth/login/', {'username': 'testuser_1', 'password': '123456qwerty'})

        response = client.get('/subscriptions/')

        assert response.status_code == 200, (
            'Страница `/subscriptions/` не найдена, проверьте этот адрес в *urls.py*'
        )

        response = client.get(f'author/{user}/follow/')

        assert count == Follow.objects.count(), (
            f'Проверьте, что при POST запросе на `author/{user}/follow/` с подпиской автора на самого себя, количество записей в модель не меняется'
        )

        response = client.get(f'author/{user_2}/follow/')
        assert response.status_code == 302
        assert response['Location'] == reverse('blog:subscriptions'), (
            f'Проверьте, что при POST запросе на `author/{user_2}/follow/` с правильными данными идет перенаправление на страниц с подписками'
        )

        assert count - 1 == Follow.objects.count(), (
            f'Проверьте, что при POST запросе на `author/{user_2}/follow/` подписка удаляется'
        )


