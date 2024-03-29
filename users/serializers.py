from django.db.models import QuerySet, Sum
from rest_framework import serializers

from games.models import Game, Score
from users.models import User


class UserGameSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()

    def get_scores(self, game: Game) -> int:
        return Score.objects.filter(game=game).aggregate(Sum('score'))['score__sum']

    class Meta:
        model = Game
        fields = ('slug', 'title', 'description', 'thumbnail', 'scores')


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('slug', 'title', 'description')


class ScoreSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    timestamp = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Score
        fields = ('score', 'timestamp', 'game')


class UserSerializer(serializers.ModelSerializer):
    registered_timestamp = serializers.DateTimeField(source='created_at')
    highscores = ScoreSerializer(many=True, source='scores')

    authored_games = serializers.SerializerMethodField()

    def get_authored_games(self, user: User) -> QuerySet:
        filters = {
            'author': user,
        }
        current_user = self.context['user']
        if current_user != user:
            filters['gameversion__version__gte'] = 1

        games = Game.objects.filter(**filters)
        serializer = UserGameSerializer(games, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('username', 'registered_timestamp', 'authored_games', 'highscores')
