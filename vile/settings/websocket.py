#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://django-websocket-redis.readthedocs.io/en/latest/installation.html
WEBSOCKET_URL = '/stream/'

WS4REDIS_EXPIRE = 10

# WS4REDIS_SUBSCRIBER = 'stream..RedisStore'

WS4REDIS_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
    'password': '',
}
