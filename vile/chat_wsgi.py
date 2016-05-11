"""
WSGI config for vile project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import gevent.socket
import redis.connection
redis.connection.socket = gevent.socket
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vile.settings")

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer

application = uWSGIWebsocketServer()
