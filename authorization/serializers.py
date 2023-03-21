from datetime import datetime

import django.db.utils
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from . import exceptions


class BaseSignSerializer(serializers.ModelSerializer):
    @property
    def data(self) -> dict:
        self._user.last_login = datetime.utcnow()
        self._user.save()

        refresh_token = RefreshToken.for_user(self._user)
        return {
            'status': 'success',
            'token': str(refresh_token),
        }

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpSerializer(BaseSignSerializer):
    username = serializers.CharField(min_length=4, max_length=60, required=True)
    password = serializers.CharField(min_length=8, max_length=2**16, required=True)

    def save(self) -> User:
        username, password = self.validated_data['username'], self.validated_data['password']
        encoded_password = make_password(password)
        try:
            self._user = User.objects.create(username=username, password=encoded_password)
        except django.db.utils.IntegrityError:
            raise exceptions.UserAlreadyExists()

        return self._user


class SignInSerializer(BaseSignSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data: dict) -> User:
        username, password = data['username'], data['password']
        try:
            self._user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.InvalidCredentials()

        if self._user.is_blocked:
            raise exceptions.UserBlocked(self._user.block_reason)

        if check_password(password, self._user.password):
            return self._user

        raise exceptions.InvalidCredentials()
