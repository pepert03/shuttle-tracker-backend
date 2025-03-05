import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import DriverLocation


class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("location_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("location_updates", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude, longitude = data["latitude"], data["longitude"]

        # Guardar la ubicación en la base de datos
        DriverLocation.objects.create(latitude=latitude, longitude=longitude)

        # Enviar la ubicación a todos los clientes conectados
        await self.channel_layer.group_send(
            "location_updates",
            {
                "type": "send_location",
                "latitude": latitude,
                "longitude": longitude,
            },
        )

    async def send_location(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "latitude": event["latitude"],
                    "longitude": event["longitude"],
                }
            )
        )
