# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import datetime

from celery import states
from celery.schedules import crontab

from aio_client import configs as aio_client_settings
from aio_client.base.helpers import get_not_sent_post_list
from aio_client.base.tasks import PeriodicAsyncTask
from aio_client.base.tasks import TaskContextManager
from aio_client.consumer.helpers import consumer_delete_receipt
from aio_client.consumer.helpers import consumer_delete_request
from aio_client.consumer.helpers import consumer_get_receipt
from aio_client.consumer.helpers import consumer_get_requests
from aio_client.consumer.helpers import consumer_post_request

from .models import PostConsumerRequest


class GetAllReceiptsConsumerTask(PeriodicAsyncTask):
    """Задача на получение ответа от СМЭВ по всем отправленным заявкам.

    По каждой заявке отправляем запрос на удаление полученных ответов из AIO.
    """

    description = (u"AIO клиент поставщик. "
                   u"Получение ответа СМЭВ по всем отправленным заявкам.")
    stop_executing = False
    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"
    abstract = not aio_client_settings.CONSUMER_ON
    if aio_client_settings.CONSUMER_ON:
        run_every = crontab(
            minute=aio_client_settings.CS_REC_TASK_EVERY_MINUTE,
            hour=aio_client_settings.CS_REC_TASK_EVERY_HOUR)
    else:
        run_every = None

    def run(self, *args, **kwargs):
        super(GetAllReceiptsConsumerTask, self).run(*args, **kwargs)
        values = {
            u"Время начала": datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT),
        }
        self.set_progress(
            progress=u"Получение ответа СМЭВ по всем отправленным заявкам...",
            values=values
        )
        messages = []
        with TaskContextManager(
                values, u'При получении ответов произошла ошибка'):
            messages = consumer_get_receipt()

        values[u'Кол-во сообщений'] = str(len(messages))
        for message in messages:
            message_id = message.get('message_id')
            values[u'Сообщение %s' % message_id] = (
                u'Отправка запроса на удаление полученных ответов от СМЭВ')
            with TaskContextManager(
                    values,
                    (u'Не удалось отправить запрос на удаление сообщения %s'
                    % message_id)):
                consumer_delete_receipt(message_id)

        values[u"Время окончания"] = datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT)
        self.set_progress(
            progress=u'Завершено',
            task_state=states.SUCCESS,
            values=values)

        return self.state


class GetAllResponsesConsumerTask(PeriodicAsyncTask):
    """Задача на получение всех ответов из очереди СМЭВ.

    По каждому ответу отправляем запрос на его удаление из AIO.
    """

    description = (u"AIO клиент поставщик. "
                   u"Получение всех ответов из очереди СМЭВ.")
    stop_executing = False
    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"
    abstract = not aio_client_settings.CONSUMER_ON
    if aio_client_settings.CONSUMER_ON:
        run_every = crontab(
            minute=aio_client_settings.CS_RES_TASK_EVERY_MINUTE,
            hour=aio_client_settings.CS_RES_TASK_EVERY_HOUR)
    else:
        run_every = None

    def run(self, *args, **kwargs):
        super(GetAllResponsesConsumerTask, self).run(*args, **kwargs)
        values = {
            u"Время начала": datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT),
        }
        self.set_progress(
            progress=u"Получаем ответа СМЭВ по всем отправленным заявкам ...",
            values=values)

        messages = []
        with TaskContextManager(
                values, u'При получении ответа СМЭВ произошла ошибка'):
            messages = consumer_get_requests()

        values[u'Кол-во ответов'] = str(len(messages))

        for message in messages:
            message_id = message.get('message_id')
            values[u'Сообщение %s' % message_id] = (
                u'Отправка запроса на удаление полученного ответа от СМЭВ в АИО'
            )
            with TaskContextManager(
                    values,
                    (u'Не удалось отправить запрос на удаление полученного '
                     u'ответа от СМЭВ %s' % message_id)):
                consumer_delete_request(message_id)

        # проверка наличия сообщений пост на повторную отправку
        not_sent_post_list = get_not_sent_post_list(PostConsumerRequest)
        if not_sent_post_list:
            values[u'Найдено %d заявок РИС на повторную отправку'
                   % len(not_sent_post_list)] = u''
            for request_msg in not_sent_post_list:
                consumer_post_request(request_msg)

        values[u"Время окончания"] = datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT)
        self.set_progress(
            progress=u'Завершено',
            task_state=states.SUCCESS,
            values=values)

        return self.state
