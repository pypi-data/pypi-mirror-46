# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from aio_client.base import RequestTypeEnum
from aio_client.base import _prepare_log
from aio_client.base import send_request
from aio_client.base.helpers import create_message_id
from aio_client.base.helpers import post_request

from .models import GetConsumerReceipt
from .models import GetConsumerResponse
from .models import PostConsumerRequest


def consumer_get_requests():
    """Получение всех ответов из очереди СМЭВ
    :return list список словарей с параметрами ответа
    """
    request_log = _prepare_log(RequestTypeEnum.CS_GET)

    response = send_request(request_log)
    for message in response.json():
        message['request_id'] = request_log
        GetConsumerResponse.objects.create(**message)
    return response.json()


def consumer_delete_request(message_id):
    """Запрос на удаление полученных ответов
    :param string message_id: идетификатор заявки
    :return: инстанс класса requests.models.Response
    """
    request_log = _prepare_log(RequestTypeEnum.CS_DEL)
    request_log.http_body = message_id
    response = send_request(request_log)
    return response


def consumer_post_request(request_msg):
    """Передача заявок в СМЭВ

    Если сообщение отправляется повторно, то создаем message_id заново
    :param request_msg: объект класса PostConsumerRequest
     c параметрами ответа
    :return: инстанс класса requests.models.Response, либо None
    """
    assert isinstance(request_msg, PostConsumerRequest)
    if hasattr(request_msg, 'request_id'):
        request_msg.message_id = create_message_id()
    return post_request(request_msg)


def consumer_get_receipt():
    """Получение ответа СМЭВ по всем отправленным заявкам
    :return dict словарь с параметрами ответа
    """
    request_log = _prepare_log(RequestTypeEnum.CS_GET_R)
    response = send_request(request_log)
    for message in response.json():
        message['request_id'] = request_log
        GetConsumerReceipt.objects.create(**message)
    return response.json()


def consumer_delete_receipt(message_id):
    """Запрос на удаление полученных ответов от СМЭВ
    :param string message_id: идентификатор ответа
    :return инстанс класса requests.models.Response
    """
    request_log = _prepare_log(RequestTypeEnum.CS_DEL_R)
    request_log.http_body = message_id
    response = send_request(request_log)
    return response
