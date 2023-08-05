# coding:utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from functools import wraps
from uuid import uuid1
import json

from django.core.exceptions import ValidationError
import celery
import dateutil.parser
import django


MIN_SUPPORTED_VERSION = (1, 4)
MAX_SUPPORTED_VERSION = (1, 11)


def convert(s):
    """Преобразует строку в datetime."""
    return dateutil.parser.parse(s)


def to_str_decorator(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result)
    return wrapper


uuid = to_str_decorator(uuid1)


def register_task(task):
    """Регистрирует задание в Celery.

    Начиная с Celery 4.x появилась необходимость регистрировать задания,
    основанные на классах с помощью метода
    :meth:`~celery.app.base.Celery.register_task`. В более ранних версиях
    Celery задания регистрируются автоматически.

    :rtype: celery.app.task.Task
    """
    if celery.VERSION < (4, 0, 0):
        return task

    elif celery.VERSION == (4, 0, 0):
        # В Celery 4.0.0 нет метода для регистрации заданий,
        # исправлено в 4.0.1
        raise Exception(u'Use Celery 4.0.1 or later.')

    else:
        app = celery.app.app_or_default()
        return app.register_task(task)


def validate_json(value):
    """Проверяет на валидность json формату."""
    try:
        json.loads(value)
    except Exception:
        raise ValidationError(
            'Невозможно преобразовать данные о вложениях {}'.format(value)
        )


def change_choices(model, field_name, choices):
    """Подменяет список `choices` для поля модели.

    :param model: Модель приложения.
    :param field_name: Название поля модели.
    :param choices: Список `choices`
    """
    field = model._meta.get_field(field_name)
    if django.VERSION[:2] < (1, 9):
        choices_attr = '_choices'
    else:
        choices_attr = 'choices'

    setattr(field, choices_attr, choices)


def change_app_label(app_label):
    """Заменяет значение ``app_label`` в мета-данных модели.

    Сделано для совместимости с South миграциями.
    :param app_label: Новое имя
    """
    if django.VERSION[:2] < (1, 7):
        return app_label


def get_last_object(queryset):
    """Возвращает последнее значение из выборки.

    Сделано для совместимости с Django<1.6
    :param queryset: Выборка
    :return: Значение из выборки
    """
    if django.VERSION[:2] >= (1, 6):
        return queryset.last()

    result = None
    objects = list(
        (
            queryset.reverse()
            if queryset.ordered else queryset.order_by('-pk')
        )[:1]
    )
    if objects:
        result = objects[0]

    return result


def get_model(app_label, model_name):
    """Возвращает класс модели.

    :param str app_label: Имя приложения модели.
    :param str model_name: Имя модели (без учета регистра символов).

    :rtype: :class:`django.db.models.base.ModelBase`
    """
    if MIN_SUPPORTED_VERSION <= django.VERSION[:2] <= (1, 6):
        from django.db.models.loading import get_model as get_model_
        result = get_model_(app_label, model_name)
    else:
        from django.apps import apps
        result = apps.get_model(app_label, model_name)

    return result


def noop_operation():
    """Возвращает заглушку для операции в миграциях.

    Сделано для совместимости с Django 1.7
    """
    def noop(apps, schema_editor):
        return

    if django.VERSION[:2] == (1, 7):
        return noop
    else:
        from django.db import migrations
        return migrations.RunPython.noop
