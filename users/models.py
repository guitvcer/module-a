from datetime import datetime

from django.db import models


class User(models.Model):
    class BlockReasonChoices(models.TextChoices):
        BY_ADMIN = 'You have been blocked by an administrator'
        BY_CHEATING = 'You have been blocked for cheating'
        BY_SPAMMING = 'You have been blocked for spamming'

    username = models.CharField(max_length=60, unique=True, verbose_name='Username')
    password = models.CharField(max_length=2**16, verbose_name='Password')

    is_active = models.BooleanField(default=True, verbose_name='Is Active?')

    is_blocked = models.BooleanField(default=False, verbose_name='Is Blocked?')
    block_reason = models.CharField(
        max_length=128, choices=BlockReasonChoices.choices,
        null=True, blank=True, verbose_name='Block Reason')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_login = models.DateTimeField(verbose_name='Last Login')

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs) -> None:
        if not self.last_login:
            self.last_login = datetime.utcnow()

        super().save(*args, **kwargs)
