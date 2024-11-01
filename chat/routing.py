from django.urls import re_path
from . import consumers

websocket_urlpatterns = [ 
    re_path(r"chat\/(?P<id>\d+)\/", consumers.Consumer.as_asgi()),
    #re_path(r"chat/", consumers.Consumer.as_asgi()),
]



""" {% for messages in messages %}
         <div class = "popup">
            <p class = "user">{{message.writer}}</p>
            <p class = "text">{{message.content}}</p>
            <p class = "date">{{message.datetime}}</p>
         </div>
    {% endfor %}  """