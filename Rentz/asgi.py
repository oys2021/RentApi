
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rentz.settings')
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
# application = get_asgi_application()
import chat.routing
application=ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':
    URLRouter(chat.routing.websocket_urlpatterns)
})

