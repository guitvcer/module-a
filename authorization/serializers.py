from django.contrib.auth.hashers import check_password, make_password
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
        encoded_password = make_password(password)
        user = User.objects.create(username=username, password=encoded_password)

        return user

    def get(self) -> User:
        username, password = self.validated_data['username'], self.validated_data['password']
        user = User.objects.get(username=username)

        encoded_password = make_password(password)
        check_password(user.password, encoded_password)

        return user
