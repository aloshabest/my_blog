from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Ytube:groups', kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.CharField(max_length=2000)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Ytube:author', kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, verbose_name='Автор')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    # category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    # tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Ytube:post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.slug = gen_slug(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cтатья'
        verbose_name_plural = 'Статьи'





