# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import models
from django.db.models import Max

from aio_client.base.models import GetReceipt
from aio_client.base.models import RequestLog
from aio_client.base.models import RequestMessage


class PostConsumerRequestManager(models.Manager):

    def not_sent(self):
        """Получаем те записи об отправке сообщения,
        где последняя попытка не удачная, статус НЕ ОТПРАВЛЕН"""
        # Список записей о последней попытке отправки сообщений
        qs_last_requests = PostConsumerRequest.objects.values(
            'message_id').annotate(max_id=Max('id'))
        # получаем те записи об отправке сообщения,
        # где последняя попытка не удачная
        qs_errors = PostConsumerRequest.objects.filter(
            id__in=qs_last_requests.values_list('max_id', flat=True),
            request_id__state=RequestLog.NOT_SENT).exclude(
            request_id__error__exact='')
        return qs_errors


class PostConsumerRequest(RequestMessage):
    """Передача заявок в СМЭВ"
    message_id Уникальный идентификатор запроса с типом данных UUID,
    который формируется в РИС по  RFC 4122 первого типа
    """
    NAME_ID_FIELD = "message_id"
    LIST_AIO_FIELDS = [
        "message_id",
        "body",
        "attachments",
        "message_type",
        "is_test_message",
    ]
    is_test_message = models.BooleanField(
        default=False, verbose_name=u'Признак тестового взаимодействия')
    # Стандартный менеджер.
    objects = PostConsumerRequestManager()

    class Meta:
        verbose_name = u'Поставщик. Заявки в СМЭВ'
        app_label = 'aio_client'


class GetConsumerResponse(RequestMessage):
    """Ответы из очереди СМЭВ"""
    LIST_AIO_FIELDS = [
        "message_id",
        "origin_message_id",
        "body",
        "attachments",
        "message_type",
    ]

    class Meta:
        verbose_name = u'Поставщик. Ответ СМЭВ'
        app_label = 'aio_client'


class GetConsumerReceipt(GetReceipt):
    """Квитанций с результатом отправки запроса"""
    LIST_AIO_FIELDS = (
        "message_id",
        "error",
        "origin_message_id",
        "fault",
        "message_type",
    )

    class Meta:
        verbose_name = u'Поставщик. Ответ СМЭВ по заявкам'
        app_label = 'aio_client'
