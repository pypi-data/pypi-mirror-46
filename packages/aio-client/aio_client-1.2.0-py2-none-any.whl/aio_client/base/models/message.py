# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json

from django.db import models
import six

from aio_client.utils import validate_json

from .base import AbstractStateModel
from .log import RequestLog


class AbstractMessage(AbstractStateModel):
    request_id = models.ForeignKey(RequestLog, verbose_name=u"Лог запроса")
    message_type = models.CharField(
        max_length=100, verbose_name=u"Вид сведений")
    message_id = models.CharField(
        max_length=100, null=True,
        verbose_name=u"Уникальный идентификатор сообщения")
    origin_message_id = models.CharField(
        max_length=100,
        null=True,
        verbose_name=u"Уникальный идентификатор цепочки взаимодействия в АИО")

    class Meta:
        abstract = True
        ordering = ['-id', ]

    def __str__(self):
        return '{0} - {1}'.format(self.message_id or '',
                                  self.origin_message_id or '')


class RequestMessage(AbstractMessage):
    NAME_ID_FIELD = "origin_message_id"
    body = models.TextField(verbose_name=u"Бизнес-данные запроса")
    attachments = models.TextField(
        verbose_name="Вложения запроса",
        default='[]',
        blank=True,
        validators=[validate_json]
    )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             **kwargs):
        """Сохраняет с дополнительной проверкой для вложений запроса."""
        if not isinstance(self.attachments, six.string_types):
            self.attachments = json.dumps(self.attachments)
        super(RequestMessage, self).save(
            force_insert, force_update, using, **kwargs
        )


class GetReceipt(AbstractMessage):
    NAME_ID_FIELD = "origin_message_id"
    error = models.TextField(
        default='',
        verbose_name=u"Сообщение об ошибке, "
                     u"возникшей при передаче данных в СМЭВ")
    fault = models.BooleanField(
        default=False, verbose_name=u"Признак успешного взаимодействия")

    class Meta:
        abstract = True
