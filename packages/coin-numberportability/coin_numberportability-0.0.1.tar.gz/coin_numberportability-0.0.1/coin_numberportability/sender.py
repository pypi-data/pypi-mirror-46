import requests

import config
import numberportability.securityservice as securityservice
from coin_numberportability.domain import MessageType
from coin_numberportability.messages.message_response import MessageResponse
from coin_numberportability.utils import json2obj, handle_http_error


def send_message(message):
    message_type = message.get_message_type()
    message_dict = message.to_dict()
    url = f'{config.apiUrl}/{message_type.value}'
    return _send_request(requests.post, url, message_dict)


def confirm(transaction_id):
    url = f'{config.apiUrl}/{MessageType.CONFIRMATION_V1.value}/{transaction_id}'
    json = {'transactionId': transaction_id}
    return _send_request(requests.put, url, json)


def _send_request(request, url, json):
    method = request.__name__
    security_service = securityservice.securityService
    headers = security_service.generate_headers(url, method, json)
    cookie = security_service.generate_jwt()
    response = request(url, json=json, headers=headers, cookies=cookie)
    handle_http_error(response)
    response_json = json2obj(response.text)
    try:
        return MessageResponse(response_json.transaction_id)
    except AttributeError:
        return response_json
