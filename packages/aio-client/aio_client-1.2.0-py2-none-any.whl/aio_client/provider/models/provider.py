# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import models
from django.db.models import Max

from aio_client.base.models import GetReceipt
from aio_client.base.models import RequestLog
from aio_client.base.models import RequestMessage
from aio_client.utils import change_choices


class GetProviderRequest(RequestMessage):
    """ответ на запрос получение всех заявок к РИС"""
    # Список полей приходящих из АИО
    NOT_SENT = 1
    SENT = 2
    ERROR = 3

    STATE = (
        (NOT_SENT, u'Не отправлен в РИС'),
        (SENT, u'Отправлен в РИС'),
        (ERROR, u'Ошибка'),
    )
    LIST_AIO_FIELDS = (
        "message_id",
        "origin_message_id",
        "body",
        "attachments",
        "is_test_message",
        "replay_to",
        "message_type")
    is_test_message = models.BooleanField(
        default=False, verbose_name=u'Признак тестового взаимодействия')
    replay_to = models.CharField(
        max_length=100, verbose_name=u'Индекс сообщения в СМЭВ')

    class Meta:
        verbose_name = u'Провайдер. Заявки от СМЭВ'
        app_label = 'aio_client'


change_choices(GetProviderRequest, 'state', GetProviderRequest.STATE)
GetProviderRequest._meta.get_field('state').default = (
    GetProviderRequest.NOT_SENT
)


class PostProviderRequestManager(models.Manager):

    def not_sent(self):
        """Получаем те записи об отправке сообщения,
        где последняя попытка не удачная, статус НЕ ОТПРАВЛЕН"""
        # Список записей о последней попытке отправки сообщений
        qs_last_requests = PostProviderRequest.objects.values(
            'origin_message_id').annotate(max_id=Max('id'))
        # получаем те записи об отправке сообщения,
        # где последняя попытка не удачная
        qs_errors = PostProviderRequest.objects.filter(
            id__in=qs_last_requests.values_list('max_id', flat=True),
            request_id__state=RequestLog.NOT_SENT).exclude(
            request_id__error__exact='')
        return qs_errors


class PostProviderRequest(RequestMessage):
    """ответ РИС как поставщика на заявку из АИО"""
    # Список полей в сообщение, которые ожидает АИО
    LIST_AIO_FIELDS = (
        "origin_message_id",
        "body",
        "message_type",
        "attachments",
        "content_failure_code",
        "content_failure_comment",
        "replay_to",
        "is_test_message"
    )

    ACCESS_DENIED = 'ACCESS_DENIED'
    UNKNOWN_REQUEST_DESCRIPTION = 'UNKNOWN_REQUEST_DESCRIPTION'
    NO_DATA = 'NO_DATA'
    FAILURE = 'FAILURE'

    FAILURE_CODES = (
        (ACCESS_DENIED, 'access denied'),
        (UNKNOWN_REQUEST_DESCRIPTION, 'unknown request description'),
        (NO_DATA, 'no data'),
        (FAILURE, 'failure'),
    )
    # используется как "обратный адрес" при передаче ответа на заявку
    replay_to = models.CharField(
        max_length=4000, verbose_name=u'Индекс сообщения в СМЭВ')
    content_failure_code = models.CharField(
        max_length=50,
        choices=FAILURE_CODES,
        null=True,
        blank=True,
        verbose_name=u'Код причины отказа'
    )
    content_failure_comment = models.TextField(
        default='', blank=True, verbose_name=u'Пояснение причины отказа')
    is_test_message = models.BooleanField(
        default=False, verbose_name=u'Признак тестового взаимодействия')
    # Стандартный менеджер.
    objects = PostProviderRequestManager()

    class Meta:
        verbose_name = u'Провайдер. Ответ на заявку'
        app_label = 'aio_client'


class GetProviderReceipt(GetReceipt):
    """Ответы из очереди СМЭВ"""
    # Список полей приходящих из АИО
    LIST_AIO_FIELDS = (
        "message_id",
        "error",
        "origin_message_id",
        "fault",
        "message_type",
    )

    class Meta:
        verbose_name = u'Провайдер. Ответ СМЭВ по заявкам'
        app_label = 'aio_client'
