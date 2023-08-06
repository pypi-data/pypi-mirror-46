import json
from collections import namedtuple
from http import HTTPStatus
from json import JSONDecodeError

import requests

from coin_numberportability.messages.common import ErrorMessage


def _json_object_hook(d):
    return namedtuple('np', d.keys())(*d.values())


def json2obj(data):
    try:
        return json.loads(data, object_hook=_json_object_hook)
    except JSONDecodeError:
        return data


def handle_http_error(response):
    status = response.status_code
    if status == HTTPStatus.OK:
        return
    description = HTTPStatus(status).description
    try:
        error_message = json2obj(response.text)
        error_object = ErrorMessage(error_message.transaction_id, error_message.errors)
        raise requests.HTTPError(f'HTTP Status: {status}, {description}\n{str(error_object)}', response=error_object)
    except AttributeError:
        raise requests.HTTPError(f'HTTP Status: {status}, {description}', response=response)
