from abc import abstractmethod, ABC
from json import JSONDecodeError

import requests
import sseclient

import config
import numberportability.securityservice as securityservice
from coin_numberportability.domain import MessageType, ConfirmationStatus
from coin_numberportability.sender import confirm
from coin_numberportability.utils import json2obj, handle_http_error


class Receiver(ABC):
    @staticmethod
    def _get_stream(url, offset: int, confirmation_status: ConfirmationStatus, message_types: [MessageType]):
        params = {
            'offset': offset,
            'messageTypes': message_types and ','.join([message_type.value for message_type in message_types]),
            'confirmationStatus': confirmation_status and confirmation_status.value
        }
        security_service = securityservice.securityService
        headers = security_service.generate_headers(url)
        cookie = security_service.generate_jwt()
        return requests.get(url, stream=True, headers=headers, cookies=cookie, params=params)

    def start_stream(self, offset: int = None, confirmation_status: ConfirmationStatus = None, message_types: [MessageType] = None):
        response = self._get_stream(config.sseUrl, offset, confirmation_status, message_types)
        handle_http_error(response)
        client = sseclient.SSEClient(response)
        for event in client.events():
            if event.data:
                try:
                    event_type: str = event.event.lower()
                    data = json2obj(event.data).message
                    message_id = event.id
                    if event_type == MessageType.PORTING_REQUEST_V1.get_event_type():
                        self.on_porting_request(message_id, data)
                    elif event_type == MessageType.PORTING_REQUEST_ANSWER_V1.get_event_type():
                        self.on_porting_request_answer(message_id, data)
                    elif event_type == MessageType.PORTING_REQUEST_ANSWER_DELAYED_V1.get_event_type():
                        self.on_porting_request_answer_delayed(message_id, data)
                    elif event_type == MessageType.PORTING_PERFORMED_V1.get_event_type():
                        self.on_porting_performed(message_id, data)
                    elif event_type == MessageType.DEACTIVATION_V1.get_event_type():
                        self.on_deactivation(message_id, data)
                    elif event_type == MessageType.CANCEL_V1.get_event_type():
                        self.on_cancel(message_id, data)
                    elif event_type == MessageType.ERROR_FOUND_V1.get_event_type():
                        self.on_error_found(message_id, data)
                    else:
                        raise ValueError(f"Number Portability Message with the following content isn't supported: {event}")
                except (JSONDecodeError, AttributeError):
                    raise ValueError(f"Conversion of Number Portability Message failed for the following event: {event}")

    @abstractmethod
    def on_porting_request(self, message_id, message):
        pass

    @abstractmethod
    def on_porting_request_answer(self, message_id, message):
        pass

    @abstractmethod
    def on_porting_request_answer_delayed(self, message_id, message):
        pass

    @abstractmethod
    def on_porting_performed(self, message_id, message):
        pass

    @abstractmethod
    def on_deactivation(self, message_id, message):
        pass

    @abstractmethod
    def on_cancel(self, message_id, message):
        pass

    @abstractmethod
    def on_error_found(self, message_id, message):
        pass
