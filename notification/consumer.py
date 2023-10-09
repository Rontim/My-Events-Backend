import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.event_group_name = None

    async def connect(self):
        self.event_group_name = self.scope['url_route']['kwargs']['event_slug']
        self.user = self.scope['user']
        if not self.user.is_anonymous:
            await self.channel_layer.group_add(
                self.event_group_name, self.channel_name)
            await self.accept()
            print('Connection accepted')

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.event_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        print(text_data_json)


class BroadCastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass
