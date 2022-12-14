# Generated by Django 4.1 on 2022-08-17 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
