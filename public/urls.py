from django.conf.urls import url
from public.views import create_club, club_homepage, club_post


urlpatterns = [
    url(r'create$', create_club, name='create'),
    url(r'(?P<id>\d+)$', club_homepage, name='home'),
    url(r'(?P<id>\d+)/post$', club_post, name='post'),
]
