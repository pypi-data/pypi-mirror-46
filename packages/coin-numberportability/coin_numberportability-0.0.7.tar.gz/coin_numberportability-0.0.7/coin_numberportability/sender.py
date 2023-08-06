import logging

import requests

from coin_numberportability.config import config
from coin_numberportability.domain import MessageType
from coin_numberportability.messages.message_response import MessageResponse
from coin_numberportability.securityservice import security_service
from coin_numberportability.utils import json2obj, handle_http_error

logger = logging.getLogger(__name__)


def send_message(message):
    logger.info(f'Sending message: {message}')
    message_type = message.get_message_type()
    message_dict = message.to_dict()
    url = f'{config.apiUrl}/{message_type.value}'
    logger.debug(f'url: {url}')
    return _send_request(requests.post, url, message_dict)


def confirm(transaction_id):
    logger.info(f'Sending conformation for id: {transaction_id}')
    url = f'{config.apiUrl}/{MessageType.CONFIRMATION_V1.value}/{transaction_id}'
    logger.debug(f'url: {url}')
    json = {'transactionId': transaction_id}
    return _send_request(requests.put, url, json)


def _send_request( request, url, json):
    method = request.__name__
    headers = security_service.generate_headers(url, method, json)
    cookie = security_service.generate_jwt()
    logger.info(f'Making request: {method}')
    response = request(url, json=json, headers=headers, cookies=cookie)
    logger.debug(f'Header: {response.request.headers}')
    logger.debug(f'Body: {response.request.body}')
    handle_http_error(response)
    logger.info('Converting JSON response to Python')
    response_json = json2obj(response.text)
    logger.debug(f'Response: {response_json}')
    try:
        return MessageResponse(response_json.transaction_id)
    except AttributeError:
        return response_json
