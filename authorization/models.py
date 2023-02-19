from django.db import models


class User(models.Model):
    username = models.CharField(max_length=60, verbose_name='Username')
    password = models.CharField(max_length=2**16, verbose_name='Password')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    is_blocked = models.BooleanField(default=False, verbose_name='Is Blocked?')
    is_deleted = models.BooleanField(default=False, verbose_name='Is Deleted?')
