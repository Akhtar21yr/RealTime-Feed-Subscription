from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer
import websockets
from .models import Subscription
from channels.db import database_sync_to_async

class BinanceConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.group_name = 'binance'
        user = self.scope['user']
        if  user.is_authenticated :
            try :
                is_subscribe = await self.get_user_subscription(user)
                if is_subscribe :
                    await self.channel_layer.group_add(self.group_name,self.channel_name)
                    await self.channel_layer.group_send(self.group_name,{
                        'type' : 'send.data'
                    })
                else :
                    await self.send_json({'msg':f'Please first subscribe {self.group_name} group'})
            except Exception as e :
                await self.send_json({'error':str(e)})
                await self.close()
        else :
            await self.send_json({'msg' : self.scope['error']})
            await self.close()

    async def send_data(self,event):
        try :
            async with websockets.connect(
                "wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker"
            ) as ws:
                async for data in ws:
                    await self.send_json({"data": data})
        except Exception as e :
            await self.send_json({'error':str(e)})
    

    async def receive_json(self, content, **kwargs):
        msg = content.get('message')
        if msg :
            self.send_json({'received_msg': msg})

    async def disconnect(self, code):
        raise StopConsumer()

    @database_sync_to_async
    def get_user_subscription(self, user):
        return Subscription.objects.filter(gc_name=self.group_name, user=user).exists()
