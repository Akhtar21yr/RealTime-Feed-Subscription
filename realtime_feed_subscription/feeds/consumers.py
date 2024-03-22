from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer

class BinanceConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.group_name = 'binance'
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.channel_layer.group_send(self.group_name,{
            'type' : 'send.data'
        }
        )

    async def send_data(self,event):
        await self.send_json({'msg':'msg from group'})

    async def receive_json(self, content, **kwargs):
        msg = content.get('message')
        if msg :
            self.send_json({'receive_msg': msg})

    async def disconnect(self, code):
        StopConsumer()
