from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^portable/', admin.site.urls),
]
