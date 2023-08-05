# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from django.conf import settings as dj_settings
import yaml


# Общие настройки
AIO_CLIENT_CONFIG_FILE_NAME = 'aio_client.yaml'

# переменная пути к конфигам может быть разной в разных проектах
if hasattr(dj_settings, '_CONFIG_PATH'):
    config_path = dj_settings._CONFIG_PATH
elif hasattr(dj_settings, 'CONFIG_PATH'):
    config_path = dj_settings.CONFIG_PATH
else:
    raise ValueError('Variable CONFIG_PATH is not found')


AIO_CLIENT_CONFIG = os.path.join(config_path, AIO_CLIENT_CONFIG_FILE_NAME)

cfg = yaml.load(open(AIO_CLIENT_CONFIG))
# Адрес сервера AIO
AIO_SERVER = cfg['common']['server']
# данные для аутентификации на сервере АИО
USER = cfg['common']['user']
PASSWORD = cfg['common']['password']
DEBUG_MODE = bool(cfg['common']['debugmode'])
PROVIDER_ON = bool(cfg['provider'])
CONSUMER_ON = bool(cfg['consumer'])
#настройки запуска таска "AIO клиент провайдер. Получение всех заявок к РИС."
PR_REQ_TASK_EVERY_MINUTE = cfg['celery']['provider']['request_min']
PR_REQ_TASK_EVERY_HOUR = cfg['celery']['provider']['request_hour']
#настройки запуска таска "AIO клиент провайдер.
#  Получение ответа СМЭВ по всем отправленным заявкам."
PR_REC_TASK_EVERY_MINUTE = cfg['celery']['provider']['receipt_min']
PR_REC_TASK_EVERY_HOUR = cfg['celery']['provider']['receipt_hour']

#настройки запуска таска "AIO клиент поставщик.
# Получение всех ответов из очереди СМЭВ"
CS_RES_TASK_EVERY_MINUTE = cfg['celery']['consumer']['response_min']
CS_RES_TASK_EVERY_HOUR = cfg['celery']['consumer']['response_hour']
#настройки запуска таска "AIO клиент поставщик.
#  Получение ответа СМЭВ по всем отправленным заявкам."
CS_REC_TASK_EVERY_MINUTE = cfg['celery']['consumer']['receipt_min']
CS_REC_TASK_EVERY_HOUR = cfg['celery']['consumer']['receipt_hour']
