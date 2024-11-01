from django.test import TestCase 
from channels.testing import WebsocketCommunicator 
from chat.models import Chat
from count.methods_for_tests import UnitaryTestMethods
from tricount.asgi import application
from asgiref.sync import sync_to_async
import asyncio

class ChatTest(UnitaryTestMethods):

    def setUp(self):
        self.register_someone('Tony','pwd','tony.fevrier62@gmail.com')
        self.create_a_tricount('tricount', '12', 'ff', 'EUR', 'trip', 'tony', 'marine')
        

    async def test_bdd_registering_after_message(self):
        """Send a message and see if this message was registered with correct attributes."""
        # Connect and send a message 
        communicator = WebsocketCommunicator(application, "chat/1/?user=tony") 
        connected, _= await communicator.connect() 
        self.assertTrue(connected)
        await communicator.send_json_to({"content":"test", "writer":"tony", "tricountid":1})

        # To give time to the consumer triggered by the json sending to execute before accessing the first chat object
        await asyncio.sleep(2) 

        # Verify registration in database
        chat = await sync_to_async(Chat.objects.first)()   
        self.assertEqual(chat.writer, "tony")
        self.assertEqual(chat.content, "test")
        self.assertEqual(chat.tricountid, 1)

        # Verify the return message contains good informations and disconnect
        response = await communicator.receive_json_from()
        self.assertEqual(response['writer'], "tony")
        self.assertEqual(response['content'], "test")  
        await communicator.disconnect()

    async def test_message_transmission_to_chat_html(self):
        # Connect and send a message 
        communicator = WebsocketCommunicator(application, "chat/1/?user=tony") 
        connected, _= await communicator.connect() 
        self.assertTrue(connected)
        await communicator.send_json_to({"content":"test", "writer":"tony", "tricountid":1})

        # To give time to the consumer triggered by the json sending to execute before accessing the first chat object
        await asyncio.sleep(0.1)

        response = await sync_to_async(self.client.get)('/chat/1')
        self.assertEqual(response.context['id'], 1)
        self.assertEqual(len(response.context['messages']), 1) 
        self.assertEqual(response.context['messages'][0].writer, "tony")
        self.assertEqual(response.context['messages'][0].content, "test")
