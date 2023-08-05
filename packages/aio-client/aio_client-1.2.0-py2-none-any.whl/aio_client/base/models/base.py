# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import models


class AbstractStateModel(models.Model):

    NOT_SENT = 1
    SENT = 2
    ERROR = 3

    STATE = (
        (NOT_SENT, u'Не отправлен'),
        (SENT, u'Отправлен'),
        (ERROR, u'Ошибка'),
    )

    state = models.SmallIntegerField(
        choices=STATE, default=NOT_SENT, verbose_name=u"Состояние пакетов")

    class Meta:
        abstract = True

    @staticmethod
    def get_state_name(state):
        """Вернет строковое представление состояние пакета
        :param integer state: состояние пакета
        :return: строковое наименование
        """
        for id, name in AbstractStateModel.STATE:
            if state == id:
                return name
        return u''
