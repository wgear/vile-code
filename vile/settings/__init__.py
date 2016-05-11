#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from application import *
from database import *
from auth import *
from view import *
from resource import *
from email import *
from websocket import *

if os.getenv('DEV'):
    from develop import *

INSTALLED_APPS += CUSTOM_APPS
