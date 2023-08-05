# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import django

if django.VERSION[:2] >= (1, 7):
    default_app_config = __name__ + '.apps.AioClientConfig'
