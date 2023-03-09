from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer


class SignInView(APIView):
    serializer_class = serializers.SignInSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SignOutView(APIView):
    def post(self, request: Request) -> Response:
        response = Response({'status': 'success'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
