# Generated by Django 4.1 on 2022-08-26 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ytube', '0008_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='published_posts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='Ytube.post'),
        ),
    ]
