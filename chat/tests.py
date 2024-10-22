from django.test import TestCase
from channels.testing import WebsocketCommunicator 
from chat.models import Chat
from tricount.asgi import application
from asgiref.sync import sync_to_async
import asyncio

class ChatTest(TestCase):

    async def test_bdd_registering_after_message(self):
        """Send a message and see if this message was registered with correct attributes."""
        # Connect and send a message 
        communicator = WebsocketCommunicator(application, "chat/1/?user=tony") 
        connected, _= await communicator.connect() 
        self.assertTrue(connected)
        await communicator.send_json_to({"content":"test", "writer":"tony"})

        # To give time to the consumer triggered by the json sending to execute before accessing the first chat object
        await asyncio.sleep(0.1)
        
        # Verify registration in database
        chat = await sync_to_async(Chat.objects.first)() 
        self.assertEqual(chat.writer, "tony")
        self.assertEqual(chat.content, "test")

        # Verify the return message contains good informations and disconnect
        response = await communicator.receive_json_from()
        self.assertEqual(response['writer'], "tony")
        self.assertEqual(response['content'], "test")
        self.assertEqual(response['likes'], 0) 
        await communicator.disconnect()
