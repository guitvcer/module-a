from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=60, required=True)
    password = serializers.CharField(max_length=2**16, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def save(self) -> User:
        username, password = self.validated_data['username'], self.validated_data['password']
        encrypted_password = make_password(password)
        user = User.objects.create(username=username, password=encrypted_password)

        return user
