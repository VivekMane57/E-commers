import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "E_commers.settings")

# Standard Django ASGI app
django_asgi_app = get_asgi_application()

# Import AFTER Django setup so apps are ready
from realtime.routing import websocket_urlpatterns  # noqa

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})