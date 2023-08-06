import json
import logging
from collections import namedtuple
from http import HTTPStatus
from json import JSONDecodeError

import requests

from coin_numberportability.messages.common import ErrorMessage

logger = logging.getLogger(__name__)


def _json_object_hook(d):
    return namedtuple('np', d.keys())(*d.values())


def json2obj(data):
    try:
        return json.loads(data, object_hook=_json_object_hook)
    except JSONDecodeError:
        return data


def handle_http_error(response):
    logger.info('Checking for errors')
    status = response.status_code
    logger.info(f'Http Status: {status}')
    if status == HTTPStatus.OK:
        return
    logger.error(f'Error: {response.text}')
    description = HTTPStatus(status).description
    try:
        error_message = json2obj(response.text)
        error_object = ErrorMessage(error_message.transactionId, error_message.errors)
        raise requests.HTTPError(f'HTTP Status: {status}, {description}\n{str(error_object)}', response=error_object)
    except AttributeError:
        logger.error(response)
        raise requests.HTTPError(f'HTTP Status: {status}, {description}', response=response)
