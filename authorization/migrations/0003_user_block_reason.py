# Generated by Django 4.1.7 on 2023-02-19 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_set_username_as_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='block_reason',
            field=models.CharField(choices=[('You have been blocked by an administrator', 'By Admin'), ('You have been blocked for cheating', 'By Cheating'), ('You have been blocked for spamming', 'By Spamming')], max_length=128, null=True, verbose_name='Block Reason'),
        ),
    ]