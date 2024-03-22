from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer

class BinanceConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send_json({'msg':'websocket connected'})

    async def receive_json(self, content, **kwargs):
        msg = content.get('message')
        if msg :
            self.send_json({'receive_msg': msg})

    async def disconnect(self, code):
        StopConsumer()
