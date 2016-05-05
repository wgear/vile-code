from django.conf.urls import url
from feed.views import hashtags, vote, entry_detail, comment

urlpatterns = [
    url(r'hashtags$', hashtags, name='hashtags'),
    url(r'vote$', vote, name='vote'),
    url(r'comment$', comment, name='comment'),
    url(r'view/(?P<id>\d+)', entry_detail, name='show'),
]
