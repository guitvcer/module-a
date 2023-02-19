from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers


class SignUpView(APIView):
    serializer_class = serializers.UserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)
        response = {
            'status': 'success',
            'token': str(refresh_token),
        }

        return Response(response, status=201)


class SignInView(APIView):
    serializer_class = serializers.UserSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get()

        refresh_token = RefreshToken.for_user(user)
        response = {
            'status': 'success',
            'token': str(refresh_token),
        }

        return Response(response, status=201)
