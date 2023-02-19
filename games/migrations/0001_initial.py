# Generated by Django 4.1.7 on 2023-02-19 10:14

from django.db import migrations, models
import django.db.models.deletion
import games.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authorization', '0004_remove_user_is_deleted_user_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
                ('version', models.PositiveSmallIntegerField(default=0, verbose_name='Version')),
                ('source', models.FileField(null=True, upload_to=games.models.Game._directory_path, verbose_name='Source Code')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorization.user', verbose_name='Author')),
            ],
        ),
    ]
