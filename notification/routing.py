from django.urls import path

from .consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/<str:event_slug>/notifications/",
         NotificationConsumer.as_asgi()),
]
