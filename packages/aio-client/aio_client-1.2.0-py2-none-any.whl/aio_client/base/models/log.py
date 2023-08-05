# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import json

from django.db import models

from .base import AbstractStateModel
from .enum import RequestTypeEnum


class RequestLog(AbstractStateModel):
    JSON_HEADER = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    # поле содержит иноформацию об ошибке,
    # которая произошла в процессе передачи данных
    error = models.TextField(default='', verbose_name=u"Текст ошибки запроса")
    timestamp_created = models.DateTimeField(
        auto_now_add=True, verbose_name=u"Время и дата запроса")
    request_type = models.CharField(
        max_length=100,
        choices=RequestTypeEnum.get_choices(),
        default=RequestTypeEnum.PR_GET,
        verbose_name=u"Тип запроса")
    sender_url = models.URLField(max_length=400, verbose_name=u"URL запроса")
    http_header = models.TextField(
        default=json.dumps(JSON_HEADER), verbose_name=u"Заголовок http запроса")
    http_body = models.TextField(verbose_name=u"Тело http запроса")

    class Meta:
        verbose_name = u'HTTP запрос'
        verbose_name_plural = u'HTTP запросы'
        app_label = 'aio_client'


RequestLog._meta.get_field('state').verbose_name = u"Статус запроса"
