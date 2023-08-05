# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from celery.schedules import maybe_schedule

from aio_client.base.exceptions import AioClientException
from aio_client.common.configuration import get_object


# Класс асинхронной задачи
AsyncTask = get_object("task_class")


class TaskContextManager(object):
    """Контекст менеджер для обработки исключений при работе тасков"""
    def __init__(self, values, title):
        self.values = values
        self.title = title

    def __enter__(self):
        """"""

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and issubclass(exc_type, AioClientException):
            self.values[self.title] = u'%s (код ошибки - %s)' % (
                exc_value.message, exc_value.code)
            return True


class PeriodicAsyncTask(AsyncTask):
    """Периодическая задача - это задача, которая добавляет себя в
     настройку: setting: `CELERYBEAT_SCHEDULE`"""
    abstract = True
    ignore_result = True
    relative = False
    options = None
    compat = True

    def __init__(self):
        if not hasattr(self, 'run_every'):
            raise NotImplementedError(
                'Periodic tasks must have a run_every attribute')
        self.run_every = maybe_schedule(self.run_every, self.relative)
        super(PeriodicAsyncTask, self).__init__()

    @classmethod
    def on_bound(cls, app):
        app.conf.CELERYBEAT_SCHEDULE[cls.name] = {
            'task': cls.name,
            'schedule': cls.run_every,
            'args': (),
            'kwargs': {},
            'options': cls.options or {},
            'relative': cls.relative,
        }
