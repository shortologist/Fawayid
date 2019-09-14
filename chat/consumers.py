import asyncio, json
from channels.consumer import AsyncConsumer
from django.contrib.auth.models import User
from fawayid.chat.models import Room, Message
from channels.db import database_sync_to_async


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        other_id = self.scope["url_route"]["kwargs"]["id"]
        user = self.scope["user"]
        self.room = await self.get_thread(sender=user, oid=other_id)
        self.room_name = f"Room_{self.room.id}"
        print("connect", self.room_name)
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        text = event.get("text", None)
        if text:
            data = json.loads(text)
            data["photo_url"] = self.scope["user"].profile.photo.url
            data["username"] = self.scope["user"].username
            await self.create_message(self.scope["user"], data["message"])
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message",
                    "text": json.dumps(data)
                }
            )

    async def websocket_disconnect(self, event):
        print("disconnect", event)

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    @database_sync_to_async
    def get_thread(self, sender, oid):
        other = User.objects.get(id=int(oid))
        room = Room.objects.get_or_new(user=sender, other_user=other)
        return room[0]

    @database_sync_to_async
    def create_message(self, sender, content):
        Message.objects.create(sender=sender, room=self.room, content=content)
