from django.conf.urls import url
from public.views import create_club


urlpatterns = [
    url(r'create$', create_club, name='create'),
]
