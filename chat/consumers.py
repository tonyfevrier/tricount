import json

from channels .generic.websocket import WebsocketConsumer
from chat.models import Chat

class Consumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None):
        """Handle the message received from a user posting on a chat"""
        # Recover the JSON content
        chat_object = json.loads(text_data)

        # Create a chat message 
        Chat.objects.create(writer=chat_object['writer'],
                            content=chat_object['content'])

        # Send it with date and like informations
        self.send(json.dumps(Chat.objects.first().serialize()))

        
        
    
    