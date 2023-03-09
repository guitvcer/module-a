from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers


class SignUpView(APIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)
        response = {
            'status': 'success',
            'token': str(refresh_token),
        }

        return Response(response, status=status.HTTP_201_CREATED)


class SignInView(APIView):
    serializer_class = serializers.SignInSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get()

        refresh_token = RefreshToken.for_user(user)
        response = {
            'status': 'success',
            'token': str(refresh_token),
        }

        return Response(response, status=status.HTTP_200_OK)


class SignOutView(APIView):
    def post(self, request: Request) -> Response:
        response = Response({'status': 'success'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
