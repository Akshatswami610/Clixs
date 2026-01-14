import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")

        # 🔐 Require authentication
        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # Join chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name,
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "user": self.scope["user"].id,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"],
        }))
