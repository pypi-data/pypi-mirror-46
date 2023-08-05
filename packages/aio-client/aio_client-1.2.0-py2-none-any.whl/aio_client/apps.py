# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.apps import AppConfig


class AioClientConfig(AppConfig):

    name = 'aio_client'
    label = 'aio_client'
    verbose_name = u"Клиент АИО"

    def ready(self):
        from aio_client.provider import tasks
        from aio_client.consumer import tasks
