from django.conf.urls import url
from person.views import (
    login_page, authorize, out, avatar, profile, register
)


urlpatterns = [
    url(r'login$', login_page, name='login'),
    url(r'auth$', authorize, name='auth'),
    url(r'exit$', out, name='logout'),
    url(r'avatar$', avatar, name='avatar'),
    url(r'register$', register, name='register'),
    url(r'(?P<username>.+)$', profile, name='profile')
]
