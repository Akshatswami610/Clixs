import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Clixs.settings")
django.setup()
from api.middleware import JwtAuthMiddleware
import api.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddleware(
        URLRouter(api.routing.websocket_urlpatterns)
    ),
})
