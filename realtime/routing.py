from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/shopping/(?P<room_name>[0-9a-f-]+)/$', consumers.ShoppingConsumer.as_asgi()),
    re_path(r'ws/room/(?P<room_name>\w+)/$', consumers.ShoppingConsumer.as_asgi()),  # Legacy support
]