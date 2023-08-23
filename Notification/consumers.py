from channels.generic.websocket import AsyncWebsocketConsumer
import json 

class StudentDashConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'student_dash'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # await self.notify()
    
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f'{close_code}')
    
    async def receive(self, text_data):
        print(text_data)
    

    async def notify(self):
        await self.channel_layer.group_send(self.group_name,{
            'type' : 'notify_handler',
            'message' : 'first_note'
        })
    
    async def notify_handler(self,event):
        message = event['message']
        await self.send(text_data=message)