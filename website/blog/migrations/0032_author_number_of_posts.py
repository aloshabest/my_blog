# Generated by Django 4.1 on 2022-11-03 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_alter_follow_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='number_of_posts',
            field=models.IntegerField(default=0, verbose_name='Количество постов'),
        ),
    ]
