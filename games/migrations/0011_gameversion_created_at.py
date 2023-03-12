# Generated by Django 4.1.7 on 2023-03-12 11:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_alter_score_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created At'),
            preserve_default=False,
        ),
    ]
