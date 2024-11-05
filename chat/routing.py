from django.urls import re_path
from . import consumers

websocket_urlpatterns = [ 
    re_path(r"chat\/(?P<id>\d+)\/", consumers.Consumer.as_asgi()), 
]


