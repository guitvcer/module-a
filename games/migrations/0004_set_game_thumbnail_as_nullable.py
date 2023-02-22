# Generated by Django 4.1.7 on 2023-02-21 15:11

from django.db import migrations, models
import games.models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_created_at_game_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=games.models.Game._directory_path, verbose_name='Thumbnail'),
        ),
    ]
