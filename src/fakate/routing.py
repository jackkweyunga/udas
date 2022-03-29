from fakate import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/bot/', consumers.TestBotConsumer.as_asgi()),
]