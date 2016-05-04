from django.conf.urls import url
from feed.views import hashtags

urlpatterns = [
    url(r'hashtags/$', hashtags, name='hashtags'),
]
