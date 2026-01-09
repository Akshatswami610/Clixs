import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Chat, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        URL: ws://host/ws/chat/<chat_id>/
        """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        self.user = self.scope["user"]

        # Reject unauthenticated users
        if not self.user.is_authenticated:
            await self.close()
            return

        # Check if user belongs to this chat
        is_allowed = await self.is_user_in_chat()
        if not is_allowed:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        """
        Expected payload:
        {
            "message": "Hello"
        }
        """
        try:
            data = json.loads(text_data)
            message_text = data.get("message", "").strip()

            if not message_text:
                return

            message = await self.save_message(message_text)

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "id": message.id,
                    "message": message.text,
                    "sender_id": message.sender.id,
                    "created_at": message.created_at.isoformat(),
                    "is_read": False,
                },
            )

        except Exception as e:
            await self.send(
                text_data=json.dumps({
                    "type": "error",
                    "error": str(e),
                })
            )

    async def chat_message(self, event):
        """Receive message from room group"""
        await self.send(text_data=json.dumps(event))

    # =========================
    # DB HELPERS
    # =========================

    @database_sync_to_async
    def is_user_in_chat(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            return self.user == chat.buyer or self.user == chat.seller
        except Chat.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, text):
        chat = Chat.objects.get(id=self.chat_id)

        message = Message.objects.create(
            chat=chat,
            sender=self.user,
            text=text,
            created_at=timezone.now(),
        )

        chat.last_message_at = timezone.now()
        chat.save(update_fields=["last_message_at"])

        return message
