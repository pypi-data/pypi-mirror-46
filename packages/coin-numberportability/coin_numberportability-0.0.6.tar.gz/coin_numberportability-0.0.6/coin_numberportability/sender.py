import typing

import requests

from coin_numberportability.domain import MessageType, Config
from coin_numberportability.messages.message_response import MessageResponse
from coin_numberportability.utils import json2obj, handle_http_error
from coin_numberportability.securityservice import SecurityService


class Sender:
    def __init__(self, config: typing.Type[Config]):
        self._config = config
        self._security_service = SecurityService(config)

    def send_message(self, message):
        message_type = message.get_message_type()
        message_dict = message.to_dict()
        url = f'{self._config.apiUrl}/{message_type.value}'
        return self._send_request(requests.post, url, message_dict)

    def confirm(self, transaction_id):
        url = f'{self._config.apiUrl}/{MessageType.CONFIRMATION_V1.value}/{transaction_id}'
        json = {'transactionId': transaction_id}
        return self._send_request(requests.put, url, json)

    def _send_request(self, request, url, json):
        method = request.__name__
        headers = self._security_service.generate_headers(url, method, json)
        cookie = self._security_service.generate_jwt()
        response = request(url, json=json, headers=headers, cookies=cookie)
        handle_http_error(response)
        response_json = json2obj(response.text)
        try:
            return MessageResponse(response_json.transaction_id)
        except AttributeError:
            return response_json
