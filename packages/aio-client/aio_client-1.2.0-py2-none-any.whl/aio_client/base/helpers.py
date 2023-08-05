# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import uuid

from dateutil.relativedelta import relativedelta
from django.db.models import Min
from django.forms.models import model_to_dict
from raven.contrib.django.raven_compat.models import client

from aio_client import configs as aio_client_settings
from aio_client.base import send_request
from aio_client.base.exceptions import HttpErrorException
from aio_client.base.exceptions import HttpFailureException
from aio_client.base.exceptions import TransportException
from aio_client.base.models import RequestLog
from aio_client.base.models import RequestTypeEnum
from aio_client.consumer.models import PostConsumerRequest
from aio_client.provider.models import PostProviderRequest

from .constants import EXPIRY_DATE


def create_message_id():
    """Требование СМЭВ UUID первого типа"""
    return uuid.uuid1()


def _prepare_log(request_type):
    """Заполняет поля зароса дефолтными значениями.

    :param request_type: тип запроса RequestTypeEnum
    :return: инстанс RequestLog
    """
    request_log = RequestLog()
    request_log.request_type = request_type
    request_log.sender_url = RequestTypeEnum.get_url(request_log.request_type)
    request_log.http_header = request_log.JSON_HEADER
    return request_log


def get_not_sent_post_list(class_model):
    """Возвращает список неотправленных POST запросов.

     Список сообщений PostProviderRequest/PostConsumerRequest,
     которые не смогли отправиться по причине ошибки связи(TransportException)
     Если в течение суток с момента создания запроса отправка не выполнена,
     то запросу присваивается статус error
    :return:
    """
    id_field_name = class_model.NAME_ID_FIELD
    result = []
    # Список записей о первой попытке отправки сообщений
    qs_first_requests = class_model.objects.values(
        id_field_name).annotate(min_id=Min('id'))
    # получаем те записи об отправке сообщения, где последняя попытка не удачная
    qs_errors = class_model.objects.not_sent()

    for record in qs_errors:
        value_id = getattr(record, id_field_name)
        param = qs_first_requests.get(**{id_field_name:value_id})

        date_create = class_model.objects.get(
            id=param['min_id']).request_id.timestamp_created
        # проверка что сообщение было создано более суток назад
        if ((date_create + relativedelta(days=EXPIRY_DATE)) <
                datetime.datetime.now()):
            client.captureMessage(
                u'СМЭВ. Сообщение %s=%s ВС-%s не было'
                u' отправлено в течение суток' % (
                    id_field_name, value_id, record.message_type))
            record.request_id.state = RequestLog.ERROR
            record.request_id.save()
        else:
            result.append(record)
    return result


def post_request(request_msg):
    """Отправка пост запросов
    :param request_msg: объект класса PostProviderRequest/PostConsumerRequest
     c параметрами ответа
    :return инстанс класса requests.models.Response
    """
    assert (isinstance(request_msg, PostProviderRequest) or
            isinstance(request_msg, PostConsumerRequest))

    id_field_name = request_msg.NAME_ID_FIELD

    request_msg.is_test_message = aio_client_settings.DEBUG_MODE
    request_log = _prepare_log(
        RequestTypeEnum.PR_POST
        if isinstance(request_msg, PostProviderRequest)
        else RequestTypeEnum.CS_POST)
    request_log.http_body = model_to_dict(
        request_msg,
        fields=request_msg.LIST_AIO_FIELDS)
    response = None
    try:
        response = send_request(request_log)
    except (TransportException, HttpErrorException, HttpFailureException) as exc:
        # повторная отправка пройдет позже для TransportException,
        # остальные ошибки просто отпраляем в Sentry
        client.captureMessage(
            u'СМЭВ. Сообщение %s=%s ВС-%s не было'
            u' отправлено: %s(%s)' % (
                id_field_name,
                getattr(request_msg, id_field_name),
                request_msg.message_type,
                exc.message,
                exc.code
            ))
    request_msg.request_id = request_log
    request_msg.save()
    return response
