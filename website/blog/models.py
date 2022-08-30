from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save


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
        return reverse('blog:groups', kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    title = models.CharField(max_length=255, verbose_name='Имя пользователя')
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = models.CharField(max_length=2000, verbose_name='Обо мне')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:author', kwargs={"post_slug": self.slug})

    def get_edit(self):
        return reverse('users:auth/profile', kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, slug=slugify(str(instance)), title=str(instance), description='About me....', photo='photo/2022/08/19/img_1.jpg')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.author.save()


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', blank=True, verbose_name='Фото')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Категория')
    # category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    # tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cтатья'
        verbose_name_plural = 'Статьи'




