from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
import jwt

User = get_user_model()


class CustomAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode("utf-8")
        query_param = parse_qs(query_string)
        jwt_token = query_param.get("token", [None])[0]

        if jwt_token:
            user = await self.get_user_from_token(jwt_token)
            scope["user"] = user

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            username = payload["username"]
            user = User.objects.get(username=username)

            return user

        except (jwt.ExpiredSignatureError, jwt.DecodeError, KeyError):
            pass

        return AnonymousUser()
