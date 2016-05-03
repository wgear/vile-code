from django.conf.urls import url
from person.views import login_page, authorize, out


urlpatterns = [
    url(r'login$', login_page, name='login'),
    url(r'auth$', authorize, name='auth'),
    url(r'exit', out, name='logout'),
]
