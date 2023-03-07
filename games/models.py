from django.db import models
from django.utils.text import slugify

from authorization.models import User


class Game(models.Model):

    def _directory_path(self, filename: str) -> str:
        return f'games/{self.slug}/{self.version}/{filename}'

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Author', related_name='games')

    slug = models.SlugField(verbose_name='Slug')
    title = models.CharField(max_length=60, verbose_name='Title')
    description = models.CharField(max_length=200, verbose_name='Description')

    version = models.PositiveSmallIntegerField(default=0, verbose_name='Version')
    source = models.FileField(
        upload_to=_directory_path, verbose_name='Source Code', null=True)
    thumbnail = models.ImageField(
        upload_to=_directory_path, verbose_name='Thumbnail', null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    is_active = models.BooleanField(default=True, verbose_name='Is Active?')

    def save(self, *args, **kwargs) -> "Game":
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class Score(models.Model):
    score = models.PositiveSmallIntegerField(verbose_name='Score')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Game')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='User', related_name='scores')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
