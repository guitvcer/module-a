import django.db.utils
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers

from users.models import User
from . import exceptions


class BaseSignSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=60, required=True)
    password = serializers.CharField(min_length=8, max_length=2**16, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpSerializer(BaseSignSerializer):
    def save(self) -> User:
        username, password = self.validated_data['username'], self.validated_data['password']
        encoded_password = make_password(password)
        try:
            user = User.objects.create(username=username, password=encoded_password)
        except django.db.utils.IntegrityError:
            raise exceptions.UserAlreadyExists()

        return user


class SignInSerializer(BaseSignSerializer):
    def get(self) -> User:
        username, password = self.validated_data['username'], self.validated_data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.InvalidCredentials()

        if user.is_blocked:
            raise exceptions.UserBlocked(user.block_reason)

        if check_password(password, user.password):
            return user

        raise exceptions.InvalidCredentials()
