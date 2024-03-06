from django.urls import re_path  # Use re_path for regex
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<username>[\w.]+)/$', ChatConsumer.as_asgi()),
]
