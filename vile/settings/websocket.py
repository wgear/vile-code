#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://django-websocket-redis.readthedocs.io/en/latest/installation.html
WEBSOCKET_URL = '/ws/'

WS4REDIS_EXPIRE = 3600

WS4REDIS_PREFIX = 'stream'

WS4REDIS_HEARTBEAT = '--heartbeat--'

WS4REDIS_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
    'password': '',
}
