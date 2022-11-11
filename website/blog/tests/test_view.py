import pytest
from blog.models import Group, Post, Comment, Follow, Author


class TestPost:

    @pytest.mark.django_db(transaction=True)
    def test_index(self, client, post, user):
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
            'Страница `post/slug/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_show_categories(self, client, post):
        response = client.get(f'/category/{post.group.slug}/')

        assert response.status_code == 200, (
            'Страница `/category/slug/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_authors(self, client, post):
        response = client.get('/authors/')

        assert response.status_code == 200, (
            'Страница `/authors/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_single_authors(self, client, post):
        response = client.get(f'/authors/{post.author.username}/')

        assert response.status_code == 200, (
            'Страница `/authors/author/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_new_post(self, client, user):

        post_count = Post.objects.count()

        data = {}
        response = client.post('/post/new/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/post/new/` с не правильными данными возвращается статус 400'
        )

        data = {'author': user, 'title': 'Статья номер 3', 'slug': 'stat3test', 'photo': 'photo/2022/11/03/07-4.jpg', 'group': 1}
        response = client.post('/post/new/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/post/new/` с правильными данными возвращается статус 201'
        )

        assert post_count + 1 == Post.objects.count(), (
            'Проверьте, что при POST запросе на `/post/new/` создается статья'
        )

    @pytest.mark.django_db(transaction=True)
    def test_edit(self, client, user, post):
        post_count = Post.objects.count()

        data = {}
        response = client.post(f'/post/{post.slug}/edit/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе на `/post/slug/edit/` с не правильными данными возвращается статус 400'
        )

        data = {'author': user, 'title': 'Статья номер 3', 'slug': 'stat3test', 'photo': 'photo/2022/11/03/07-4.jpg',
                'group': 1}
        response = client.post(f'/post/{post.slug}/edit/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `/post/slug/edit/` с правильными данными возвращается статус 201'
        )

        assert post_count == Post.objects.count(), (
            'Проверьте, что при POST запросе на `/post/slug/edit/` не создается новая статья, а меняется текущая'
        )

    @pytest.mark.django_db(transaction=True)
    def test_search(self, client):
        data = ['letter', 'пост', 'author']
        for item in data:
            response = client.get(f'/search/?s={item}/')

            assert response.status_code == 200, (
                'Страница `/search/` не найдена, проверьте этот адрес в *urls.py*'
            )

    @pytest.mark.django_db(transaction=True)
    def test_subscriptions(self, client, user, user_2):
        count = Follow.objects.count()

        client.post('/auth/login/', {'username': 'TestUser', 'password': '123456qwerty'})

        response = client.get('/subscriptions/')

        assert response.status_code == 200, (
            'Страница `/subscriptions/` не найдена, проверьте этот адрес в *urls.py*'
        )


        data = {'user': user, 'author': user}
        response = client.post(f'author/{user}/follow/', data=data)

        assert count == Follow.objects.count(), (
            'Проверьте, что при POST запросе на `author/user/follow/` с подпиской автора на самого себя, количество записей в модель не меняется'
        )

        assert response.status_code == 200, (
            'Страница `/subscriptions/` не найдена, проверьте этот адрес в *urls.py*'
        )

        data = {'user': user, 'author': user_2}
        response = client.post(f'author/{user}/follow/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `author/user/follow/` с правильными данными возвращается статус 201'
        )

        count = Follow.objects.count()

        data = {'user': user, 'author': user_2}
        response = client.post(f'author/{user}/unfollow/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе на `author/user/unfollow/` с правильными данными возвращается статус 201'
        )

        assert count - 1 == Follow.objects.count(), (
            'Проверьте, что при POST запросе на `author/user/follow/` подписка удаляется'
        )


