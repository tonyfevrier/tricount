import json

from channels .generic.websocket import WebsocketConsumer
from chat.models import Chat
from count.models import Counts
from asgiref.sync import async_to_sync

class Consumer(WebsocketConsumer):

    def connect(self):
        # Recover the id of the tricount from the websocket adress to create a group of discussion for participants to the tricount
        tricount_id = self.scope['url_route']['kwargs']['id']
        self.group_name = f'chat_{tricount_id}'

        # Join the channel layer for this tricount
        async_to_sync(self.channel_layer.group_add)(f'chat_{tricount_id}', self.channel_name)

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)


    def receive(self, text_data=None):
        """Handle the message received from a user posting on a chat"""
        # Recover the JSON content 
        chat_object = json.loads(text_data)   
        
        # Create a chat message  
        Chat.objects.create(writer=chat_object['writer'],
                            content=chat_object['content'],
                            tricountid=chat_object['tricountid'])  

        print(Chat.objects.all()) 
        
        # Send it with date and like informations to the group 
        async_to_sync(self.channel_layer.group_send)(self.group_name, {'type':'send.message',
                                                                        'id': Chat.objects.last().id})
        

    def send_message(self, event):
        """Handler when group_send a message"""

        # Get the id and send the serialized object 
        self.send(json.dumps(Chat.objects.get(id=event["id"]).serialize())) 


        
        
    
    