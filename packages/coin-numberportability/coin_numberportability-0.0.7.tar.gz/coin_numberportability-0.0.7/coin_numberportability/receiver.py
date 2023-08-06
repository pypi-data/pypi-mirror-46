import logging
from abc import abstractmethod, ABC
from json import JSONDecodeError

import requests
import sseclient
from requests import HTTPError

from coin_numberportability.config import config
from coin_numberportability.domain import MessageType, ConfirmationStatus
from coin_numberportability.securityservice import security_service
from coin_numberportability.utils import json2obj, handle_http_error

logger = logging.getLogger(__name__)


class Receiver(ABC):
    def _get_stream(self, url, offset: int, confirmation_status: ConfirmationStatus, message_types: [MessageType]):
        params = {
            'offset': offset,
            'messageTypes': message_types and ','.join([message_type.value for message_type in message_types]),
            'confirmationStatus': confirmation_status and confirmation_status.value
        }
        logger.debug(f'Request parameters: {params}')
        headers = security_service.generate_headers(url)
        cookie = security_service.generate_jwt()
        return requests.get(url, stream=True, headers=headers, cookies=cookie, params=params)

    def start_stream(self, offset: int = None, confirmation_status: ConfirmationStatus = None, message_types: [MessageType] = None):
        logger.info(f'Opening stream')
        response = self._get_stream(config.sseUrl, offset, confirmation_status, message_types)
        logger.debug(f'url: {response.request.url}')
        handle_http_error(response)
        client = sseclient.SSEClient(response)
        for event in client.events():
            logger.info(f'Received event')
            logger.debug(f'{event}')
            if event.data:
                try:
                    event_type: str = event.event.lower()
                    logger.info(f'Event: {event.event}')
                    data = json2obj(event.data).message
                    logger.debug(f'Message: {data}')
                    message_id = event.id
                    logger.debug(f'Message id: {message_id}')
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
                        logger.error(f"Number Portability Message with the following content isn't supported: {event}")
                except HTTPError as e:
                    logger.error(e)
                except (JSONDecodeError, AttributeError):
                    logger.error(f"Conversion of Number Portability Message failed for the following event: {event}")

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
