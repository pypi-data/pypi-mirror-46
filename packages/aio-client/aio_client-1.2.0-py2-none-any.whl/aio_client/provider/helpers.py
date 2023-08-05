# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from aio_client.base import RequestTypeEnum
from aio_client.base import _prepare_log
from aio_client.base import send_request
from aio_client.base.helpers import post_request

from .models import GetProviderReceipt
from .models import GetProviderRequest
from .models import PostProviderRequest


def provider_get_requests():
    """ Получение всех заявок к РИС
    :return list список словарей с параметрами ответа
    """
    request_log = _prepare_log(RequestTypeEnum.PR_GET)

    response = send_request(request_log)
    for message in response.json():
        message['request_id'] = request_log
        GetProviderRequest.objects.create(**message)
    return response.json()


def provider_delete_request(message_id):
    """ Запрос на удаление полученных заявок
    :param message_id: str идетификатор заявки
    :return инстанс класса requests.models.Response
    """
    request_log = _prepare_log(RequestTypeEnum.PR_DEL)
    request_log.http_body = message_id
    response = send_request(request_log)
    return response


def provider_post_request(request_msg):
    """Передача ответа на заявки
    :param request_msg: объект класса PostProviderRequest
     c параметрами ответа
    :return: инстанс класса requests.models.Response
    """
    assert isinstance(request_msg, PostProviderRequest)
    return post_request(request_msg)


def provider_get_receipt():
    """Получение ответа СМЭВ по всем отправленным заявкам
    :return dict словарь с параметрами ответа
    """
    request_log = _prepare_log(RequestTypeEnum.PR_GET_R)

    response = send_request(request_log)
    for message in response.json():
        message['request_id'] = request_log
        GetProviderReceipt.objects.create(**message)
    return response.json()


def provider_delete_receipt(message_id):
    """Запрос на удаление полученных ответов от СМЭВ
    :param string message_id: идентификатор ответа
    :return: инстанс класса requests.models.Response
    """
    request_log = _prepare_log(RequestTypeEnum.PR_DEL_R)
    request_log.http_body = message_id
    response = send_request(request_log)
    return response
