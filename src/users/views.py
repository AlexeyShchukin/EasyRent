from datetime import datetime
from django.contrib.auth import authenticate
from django.utils.timezone import make_aware

from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from src.users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is None:
            return Response(
                data={'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = Response(status=status.HTTP_200_OK)
        refresh = RefreshToken.for_user(user)

        refresh_exp = make_aware(
            datetime.fromtimestamp(refresh.payload['exp'])
        )
        access_exp = make_aware(
            datetime.fromtimestamp(refresh.access_token.payload['exp'])
        )

        response.set_cookie(
            key='refresh',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            expires=refresh_exp
        )

        response.set_cookie(
            key='access',
            value=str(refresh.access_token),
            httponly=True,
            secure=True,
            samesite='Lax',
            expires=access_exp
        )

        return response


class LogoutUserAPIView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_200_OK)
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        request.session.flush()

        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
