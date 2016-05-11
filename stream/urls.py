from django.conf.urls import url
from stream.views import PublicChat, UserChat


urlpatterns = [
    url(r'club/(?P<id>\d+)$', PublicChat.as_view(), name='public'),
    url(r'user/(?P<id>\d+)$', UserChat.as_view(), name='user'),
]
