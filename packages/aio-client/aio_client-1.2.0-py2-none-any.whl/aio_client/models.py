# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import django

if django.VERSION < (1, 7):
    from aio_client.base.models.log import RequestLog
    from aio_client.consumer.models.consumer import *
    from aio_client.provider.models.provider import *
