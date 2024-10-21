from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    #re_path(r"/chat\/\?user=\w+$", consumers.Consumer.as_asgi()),
    re_path(r"chat\/$", consumers.Consumer.as_asgi()),
]