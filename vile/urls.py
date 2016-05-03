from django.conf.urls import url, include
from django.contrib import admin
from feed.views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Home page
    url(r'^$', home, name='home'),

    # Module Feed
    url(r'^feed/', include('feed.urls', namespace='feed')),

    # Module person
    url(r'^person/', include('person.urls', namespace='person')),

    # Module Public
    url(r'^club/', include('public.urls', namespace='club')),
]
