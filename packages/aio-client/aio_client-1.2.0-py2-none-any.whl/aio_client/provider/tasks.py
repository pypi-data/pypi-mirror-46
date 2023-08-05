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
from aio_client.provider.helpers import provider_delete_receipt
from aio_client.provider.helpers import provider_delete_request
from aio_client.provider.helpers import provider_get_receipt
from aio_client.provider.helpers import provider_get_requests
from aio_client.provider.helpers import provider_post_request

from .models import PostProviderRequest


class GetAllRequestsProvideTask(PeriodicAsyncTask):
    """Задача на получение всех заявок к РИС от СМЭВ.

    Каждую заявку сохраняет в БД и отправляет запрос на удаление
    полученных заявок из AIO.
    """

    description = (u"AIO клиент провайдер. Получение всех заявок к РИС."
                   u" Отправка ответов.")
    stop_executing = False
    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"
    abstract = not aio_client_settings.PROVIDER_ON
    if aio_client_settings.PROVIDER_ON:
        run_every = crontab(
            minute=aio_client_settings.PR_REQ_TASK_EVERY_MINUTE,
            hour=aio_client_settings.PR_REQ_TASK_EVERY_HOUR)
    else:
        run_every = None

    def run(self, *args, **kwargs):
        super(GetAllRequestsProvideTask, self).run(*args, **kwargs)
        values = {
            u"Время начала": datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT),
        }
        self.set_progress(
            progress=u"Получаем все заявки к РИС в качестве поставщика ...",
            values=values
        )
        messages = []
        with TaskContextManager(values,
                                u'При получении заявок произошла ошибка'):
            messages = provider_get_requests()

        values[u'Кол-во сообщений'] = str(len(messages))
        for message in messages:
            message_id = message.get('message_id')
            values[u'Сообщение %s' % message_id] = (
                u'Отправка запроса на удаление в АИО')
            with TaskContextManager(
                    values,
                    (u'Не удалось отправить запрос на удаление сообщения %s'
                    % message_id)):
                provider_delete_request(message_id)

        # проверка наличия сообщений пост на повторную отправку
        not_sent_post_list = get_not_sent_post_list(PostProviderRequest)
        if not_sent_post_list:
            values[u'Найдено %d ответов РИС на повторную отправку'
                   % len(not_sent_post_list)] = u''
            for request_msg in not_sent_post_list:
                provider_post_request(request_msg)

        self.set_progress(
            progress=u"Получаем все заявки к РИС в качестве поставщика ...",
            values=values
        )

        values[u"Время окончания"] = datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT)

        self.set_progress(
            progress=u'Завершено',
            task_state=states.SUCCESS,
            values=values)

        return self.state


class GetAllReceiptsProvideTask(PeriodicAsyncTask):
    """Задача на получение ответа СМЭВ по всем отправленным заявкам.

    По каждому ответу отправляем запрос на его удаление из AIO.
    """

    description = (u"AIO клиент провайдер."
                   u" Получение ответа СМЭВ по всем отправленным заявкам.")
    stop_executing = False
    LOG_TIME_FORMAT = "%d.%m.%Y %H:%M"
    abstract = not aio_client_settings.PROVIDER_ON
    if aio_client_settings.PROVIDER_ON:
        run_every = crontab(
            minute=aio_client_settings.PR_REC_TASK_EVERY_MINUTE,
            hour=aio_client_settings.PR_REC_TASK_EVERY_HOUR)
    else:
        run_every = None

    def run(self, *args, **kwargs):
        super(GetAllReceiptsProvideTask, self).run(*args, **kwargs)
        values = {
            u"Время начала": datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT),
        }
        self.set_progress(
            progress=u"Получение ответа СМЭВ по всем отправленным заявкам ...",
            values=values
        )
        messages = []
        with TaskContextManager(values,
                                u'При получении ответов произошла ошибка'):
            messages = provider_get_receipt()

        values[u'Кол-во квитанций'] = str(len(messages))
        for message in messages:
            message_id = message.get('message_id')
            values[u'Сообщение %s' % message_id] = (
                u'Отправка запроса на удаление полученной квитанции '
                u'от СМЭВ в АИО'
            )
            with TaskContextManager(
                    values,
                    (u'Не удалось отправить запрос на удаление полученной'
                     u' квитанции от СМЭВ %s' % message_id)):
                provider_delete_receipt(message_id)

        values[u"Время окончания"] = datetime.datetime.now(
            ).strftime(self.LOG_TIME_FORMAT)
        self.set_progress(
            progress=u'Завершено',
            task_state=states.SUCCESS,
            values=values)

        return self.state
