from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer
import websockets

class BinanceConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.group_name = 'binance'
        user = self.scope['user']
        if user.is_authenticated :
            await self.channel_layer.group_add(self.group_name,self.channel_name)
            await self.channel_layer.group_send(self.group_name,{
                'type' : 'send.data'
            }
            )
        else :
            await self.send_json({'msg' : "Login credential not provided"})
            await self.close()

        async def send_data(self,event):
            async with websockets.connect(
                "wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker"
            ) as ws:
                async for data in ws:
                    await self.send_json({"data": data})
    

        async def receive_json(self, content, **kwargs):
            msg = content.get('message')
            if msg :
                self.send_json({'receive_msg': msg})

        async def disconnect(self, code):
            StopConsumer()
