from django.db import models
from django.utils.text import slugify

from users.models import User


class Game(models.Model):

    def _directory_path(self, filename: str) -> str:
        return f'games/{self.slug}/{self.version}/{filename}'

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Author', related_name='games')

    slug = models.SlugField(verbose_name='Slug', unique=True)
    title = models.CharField(max_length=60, verbose_name='Title')
    description = models.CharField(max_length=200, verbose_name='Description')
    thumbnail = models.ImageField(verbose_name='Thumbnail', null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    is_active = models.BooleanField(default=True, verbose_name='Is Active?')

    def __str__(self) -> str:
        return self.slug

    @property
    def last_version(self) -> 'GameVersion | None':
        return GameVersion.objects.filter(game=self).order_by('-version').first()

    def save(self, *args, **kwargs) -> "Game":
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class GameVersion(models.Model):

    def _get_source_path(self, filename: str) -> str:
        return f'games/{self.game.slug}/{self.version}/{filename}'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Game')
    version = models.PositiveSmallIntegerField(default=1, verbose_name='Version')
    source = models.FileField(upload_to=_get_source_path, verbose_name='Source Code')


class Score(models.Model):
    score = models.PositiveSmallIntegerField(verbose_name='Score')
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, verbose_name='Game', related_name='scores')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='User', related_name='scores')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
