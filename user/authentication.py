from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class CustomJWTAuthentication(JWTAuthentication):
    '''
    Custom JWT authentication class that allows to authenticate users for htttpOnly cookies
    '''

    def authenticate(self, request):
        try:
            header = self.get_header(request)

            if header is None:
                raw_token = request.COOKIES.get(settings.COOKIE_NAME)

            else:
                raw_token = self.get_raw_token(header)

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token

        except:
            return None
