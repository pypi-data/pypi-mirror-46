# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from django.forms.models import model_to_dict

from aio_client.base import RequestLog
from aio_client.utils import get_last_object

from .exceptions import ReceiptNotFound
from .exceptions import ResponseNotFound
from .helpers import provider_post_request
from .models import GetProviderReceipt
from .models import GetProviderRequest
from .models import PostProviderRequest


def get_requests(message_type=None):
    """Получение всех заявок к РИС.

    :param message_type: Вид сведений, необязательный параметр,
        если не передается, отдаем все запросы
    :return: Список запросов к РИС как к поставщику услуг
    """
    qs = GetProviderRequest.objects.exclude(
        state=GetProviderRequest.SENT)
    if message_type:
        qs = qs.filter(message_type=message_type)
    result = list(qs.values(*GetProviderRequest.LIST_AIO_FIELDS))
    qs.update(state=GetProviderRequest.SENT)
    return result


def set_error_requests(origin_message_ids):
    """Указывает признак ошибки при обработке сообщения.

    Применяется для повторного получения сообщения в get_requests.

    :param origin_message_ids: Список origin_message_id
    :return: Количество измененных записей
    """
    assert type(origin_message_ids) is list
    qs = GetProviderRequest.objects.filter(
        origin_message_id__in=origin_message_ids)
    return qs.update(state=GetProviderRequest.ERROR)


def push_request(message):
    """Передает ответ на запрос услуги.

    :param message: Запись aio_client.provider.models.PostProviderRequest
    :return: Инстанс класса requests.models.Response
    """
    assert isinstance(message, PostProviderRequest)
    response = provider_post_request(message)
    return response


def get_response(origin_message_id):
    """Запрос ответа от СМЭВ в ответ на запрос услуги.

    :param str origin_message_id: Идентификатор сообщения
    :return: Словарь со списком полей GetProviderReceipt.LIST_AIO_FIELDS
    """
    qs_response = PostProviderRequest.objects.filter(
        origin_message_id=origin_message_id,
        request_id__state=RequestLog.SENT)
    if not qs_response.exists():
        raise ResponseNotFound(
            message=ResponseNotFound.DEFAULT_MSG % origin_message_id)

    qs = GetProviderReceipt.objects.filter(
        origin_message_id=origin_message_id
    ).order_by('id')
    receipt = get_last_object(qs)
    if not receipt:
        raise ReceiptNotFound(
            message=ReceiptNotFound.DEFAULT_MSG % origin_message_id)
    return model_to_dict(receipt, GetProviderReceipt.LIST_AIO_FIELDS)
