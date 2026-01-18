# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")

        if not user or isinstance(user, AnonymousUser):
            await self.close()
            return

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        # 🔒 Authorization check
        if not await self.is_user_allowed():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    @database_sync_to_async
    def is_user_allowed(self):
        chat = Chat.objects.get(id=self.chat_id)
        return self.scope["user"] in [chat.buyer, chat.seller]

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get("message")

        if not text:
            return

        # ✅ SAVE TO DB
        message = await self.save_message(text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": {
                    "id": message.id,
                    "text": message.text,
                    "sender_id": self.scope["user"].id,
                    "created_at": message.created_at.isoformat(),
                },
            },
        )

    @database_sync_to_async
    def save_message(self, text):
        chat = Chat.objects.get(id=self.chat_id)
        return Message.objects.create(
            chat=chat,
            sender=self.scope["user"],
            text=text,
            created_at=timezone.now(),
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
