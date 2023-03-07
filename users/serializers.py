from rest_framework import serializers

from authorization.models import User
from games.models import Game
from games.serializers import GetScoreSerializer


class UserGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('slug', 'title', 'description')


class UserSerializer(serializers.ModelSerializer):
    registered_timestamp = serializers.DateTimeField(source='created_at')
    authored_games = UserGameSerializer(many=True, source='games')
    highscores = GetScoreSerializer(many=True, source='scores')

    class Meta:
        model = User
        fields = ('username', 'registered_timestamp', 'authored_games', 'highscores')
