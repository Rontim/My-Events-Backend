from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


class CustomTokenObtainPairView(TokenObtainPairView):
    '''
    Custom TokenObtainPairView that returns httpOnly cookies
    '''

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            data = {
                'detail': 'Authentication successful',
            }

            new_response = Response(data, status=status.HTTP_200_OK)

            new_response.set_cookie(
                'access',
                access_token,
                max_age=settings.COOKIE_MAX_AGE,
                path=settings.COOKIE_PATH,
                secure=settings.COOKIE_SECURE,
                httponly=settings.COOKIE_HTTP_ONLY,
                samesite=settings.COOKIE_SAMESITE
            )
            new_response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.COOKIE_MAX_AGE,
                path=settings.COOKIE_PATH,
                secure=settings.COOKIE_SECURE,
                httponly=settings.COOKIE_HTTP_ONLY,
                samesite=settings.COOKIE_SAMESITE
            )

        return new_response


class CustomTokenRefreshView(TokenRefreshView):
    '''
    Custom TokenRefreshView that returns httpOnly cookies
    '''

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']

            data = {
                'detail': 'Token refreshed',
            }

            new_response = Response(data, status=status.HTTP_200_OK)

            new_response.set_cookie(
                'access',
                access_token,
                max_age=settings.COOKIE_MAX_AGE,
                path=settings.COOKIE_PATH,
                secure=settings.COOKIE_SECURE,
                httponly=settings.COOKIE_HTTP_ONLY,
                samesite=settings.COOKIE_SAMESITE
            )

        return new_response


class CustomTokenVerifyView(TokenVerifyView):
    '''
    Custom TokenVerifyView that returns httpOnly cookies
    '''

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            data = {
                'detail': 'Token is valid',
            }

            new_response = Response(data, status=status.HTTP_200_OK)

        return new_response


class Logout(APIView):
    '''
    Logout view that clears httpOnly cookies
    '''

    def post(self, request, *args, **kwargs):
        data = {
            'detail': 'Logout successful',
        }

        response = Response(data, status=status.HTTP_200_OK)

        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
