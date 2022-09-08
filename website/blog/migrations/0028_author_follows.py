# Generated by Django 4.1 on 2022-09-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_comment_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='follows',
            field=models.ManyToManyField(related_name='followings', to='blog.author'),
        ),
    ]