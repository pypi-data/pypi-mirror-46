# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.forms.models import model_to_dict

from aio_client.base import RequestLog
from aio_client.utils import get_last_object

from .exceptions import RequestNotFound
from .helpers import consumer_post_request
from .models import GetConsumerResponse
from .models import PostConsumerRequest


def push_request(message):
    """Передача сообщения на запрос услуги.

    :param message: Запись aio_client.provider.models.PostProviderRequest
    :return: Инстанс класса requests.models.Response
    """
    assert isinstance(message, PostConsumerRequest)
    response = consumer_post_request(message)
    return response


def get_response(message_id):
    """Получение ответа от СМЭВ на Запрос услуги.

    :param str message_id: Идентификаор сообщения, котрое РИС посылает в
        теге message_id при вызове api.push_request
    :return: Словарь со списком полей GetProviderReceipt.LIST_AIO_FIELDS
    """
    qs_response = PostConsumerRequest.objects.filter(
        message_id=message_id, request_id__state=RequestLog.SENT)
    if not qs_response.exists():
        raise RequestNotFound(
            message=RequestNotFound.DEFAULT_MSG % message_id)

    qs = GetConsumerResponse.objects.filter(
        origin_message_id=message_id
    ).order_by('id')
    receipt = get_last_object(qs)
    if not receipt:
        return None
    return model_to_dict(receipt, GetConsumerResponse.LIST_AIO_FIELDS)
