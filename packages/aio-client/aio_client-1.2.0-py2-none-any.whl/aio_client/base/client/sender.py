# coding: utf-8
from requests import ConnectionError  # pylint: disable=redefined-builtin
from requests import HTTPError
from requests import Timeout
from requests import TooManyRedirects
import requests
import six

from aio_client import configs as aio_client_settings
from aio_client.base.exceptions import HttpErrorException
from aio_client.base.exceptions import HttpFailureException
from aio_client.base.exceptions import TransportException
from aio_client.base.models import DEL
from aio_client.base.models import POST
from aio_client.base.models import RequestLog
from aio_client.base.models import RequestTypeEnum


if six.PY3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin



CONNECTION_FAILED_MSG = 'Connection to recipient endpoint failed'
CONNECTION_TIMEOUT_MSG = 'Connection timeout to recipient endpoint'
TO_MANY_REDIRECTS = ('Request exceeds the configured number of'
                     ' maximum redirections')
HTTP_ERR_MSG = 'Recipient host responded with error'

# Все эти коды обозначают ошибку передачи пакета
HTTP_FAILURE_CODES = (
    500,
    502,
    503,
    504,

    400,
    401,
    403,
    404,
    # Method Not Allowed
    405
)
POST_CREATE_CODE = 201


def handling_error(method):
    def wrapper(log, *args, **kwargs):
        result = method(log, *args, **kwargs)
        if log.error and log.state == RequestLog.NOT_SENT:
            raise TransportException(log.error)
        elif log.error and log.state == RequestLog.ERROR:
            raise HttpErrorException(log.error)
        elif log.error:
            raise HttpFailureException(log.error)
        return result
    return wrapper


@handling_error
def send_request(request_log):
    """Отправка запроса в AIO
    :param request_log: Инстанс клаcса RequestLog
    :return: инстанс класса requests.models.Response
    """
    assert isinstance(request_log, RequestLog)
    response = None
    params = dict(
        method=RequestTypeEnum.get_function(request_log.request_type),
        url=request_log.sender_url,
        headers=request_log.http_header,
        auth=(aio_client_settings.USER, aio_client_settings.PASSWORD)
    )
    try:
        if params['method'] == POST:
            params['json'] = request_log.http_body
        elif params['method'] == DEL:
            params['url'] = urljoin(
                request_log.sender_url, request_log.http_body)
        response = requests.request(**params)
    except ConnectionError:
        request_log.error = CONNECTION_FAILED_MSG
    except Timeout:
        request_log.error = CONNECTION_TIMEOUT_MSG
    except TooManyRedirects:
        request_log.error = TO_MANY_REDIRECTS
    except HTTPError as err:
        request_log.error = (err.response if err.response
                             else HTTP_ERR_MSG)
        request_log.state = RequestLog.ERROR
    else:
        request_log.state = RequestLog.SENT
        if response.status_code in HTTP_FAILURE_CODES:
            request_log.error = response.content
        # пост запросы все на создание, код дб 201
        if (params['method'] == POST and
                not response.status_code == POST_CREATE_CODE):
            request_log.error = response.status_code
    request_log.save()
    return response
