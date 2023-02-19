from django.db import models


class User(models.Model):
    class BlockReasonChoices(models.TextChoices):
        BY_ADMIN = 'You have been blocked by an administrator'
        BY_CHEATING = 'You have been blocked for cheating'
        BY_SPAMMING = 'You have been blocked for spamming'

    username = models.CharField(max_length=60, unique=True, verbose_name='Username')
    password = models.CharField(max_length=2**16, verbose_name='Password')

    is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted?')

    is_blocked = models.BooleanField(default=False, verbose_name='Is Blocked?')
    block_reason = models.CharField(
        max_length=128, choices=BlockReasonChoices.choices, null=True, verbose_name='Block Reason')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
