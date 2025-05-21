import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcraft.settings")
django.setup()

players = {}
voxels = {}

class WebCraftConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.sid = self.scope['client'][1]
        players[self.sid] = {'x': 0, 'y': 0, 'z': 0, 'color': [1, 1, 1]}
        for pos, color in voxels.items():
            await self.send_json({'type': 'block_update', 'position': pos, 'color': color})
        await self.channel_layer.group_add("players", self.channel_name)

    async def disconnect(self, close_code):
        players.pop(self.sid, None)
        await self.channel_layer.group_discard("players", self.channel_name)

    async def receive_json(self, content):
        if content.get("type") == "block_update":
            pos = tuple(content['position'])
            color = content['color']
            voxels[pos] = color
            await self.channel_layer.group_send("players", {
                "type": "broadcast",
                "message": {'type': 'block_update', 'position': pos, 'color': color}
            })
        elif content.get("type") == "block_remove":
            pos = tuple(content['position'])
            voxels.pop(pos, None)
            await self.channel_layer.group_send("players", {
                "type": "broadcast",
                "message": {'type': 'block_remove', 'position': pos}
            })
        elif content.get("type") == "player_position":
            players[self.sid] = {
                'x': content['x'], 'y': content['y'], 'z': content['z'], 'color': content['color']
            }
            await self.channel_layer.group_send("players", {
                "type": "broadcast",
                "message": {
                    'type': 'player_update',
                    'players': {str(k): v for k, v in players.items()}
                }
            })

    async def broadcast(self, event):
        await self.send_json(event["message"])

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/play/", WebCraftConsumer.as_asgi()),
    ])
})
