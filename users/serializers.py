from django.db.models import QuerySet
from rest_framework import serializers

from games.models import Game
from games.serializers import GetScoreSerializer
from users.models import User


class UserGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('slug', 'title', 'description', 'thumbnail')


class UserSerializer(serializers.ModelSerializer):
    registered_timestamp = serializers.DateTimeField(source='created_at')
    highscores = GetScoreSerializer(many=True, source='scores')

    authored_games = serializers.SerializerMethodField()

    def get_authored_games(self, instance: User) -> QuerySet:
        filters = {
            'author': self.context['user'],
        }
        if self.context['user'] != instance:
            filters['version__gte'] = 1

        games = Game.objects.filter(**filters)
        serializer = UserGameSerializer(games, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('username', 'registered_timestamp', 'authored_games', 'highscores')
