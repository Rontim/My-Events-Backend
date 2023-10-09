import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from .auth import CustomAuthMiddleware

from notification import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': CustomAuthMiddleware(URLRouter(routing.websocket_urlpatterns))
    }
)
