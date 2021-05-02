"""
ASGI config for CineDate project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""


import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
import chatroom.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CineDate.settings')

"""
applicazione ASGI che dice a Channels che codice eseguire quando una
richiesta HTTP è ricevuta dal server Channels
"""
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatroom.routing.websocket_urlpatterns
        )
    ),

})
