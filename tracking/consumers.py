from channels.generic.websocket import AsyncWebsocketConsumer
import json


class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("user_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("user_group", self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get("mode") == "driver":
                await self.channel_layer.group_send(
                    "user_group",
                    {
                        "type": "location_update",
                        "latitude": data["latitude"],
                        "longitude": data["longitude"],
                    },
                )
        except Exception as e:
            print("Error en receive:", e)  # Debug

    async def location_update(self, event):
        await self.send(
            json.dumps(
                {
                    "latitude": event["latitude"],
                    "longitude": event["longitude"],
                }
            )
        )
