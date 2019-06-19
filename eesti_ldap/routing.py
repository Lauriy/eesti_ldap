from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^birthday/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', consumers.BirthdayConsumer,
            name='my_birthday'),
]

application = ProtocolTypeRouter({
    # http->django views are added by default
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
