from django.conf.urls import url
from feed.views import hashtags, vote

urlpatterns = [
    url(r'hashtags$', hashtags, name='hashtags'),
    url(r'vote$', vote, name='vote'),
]
