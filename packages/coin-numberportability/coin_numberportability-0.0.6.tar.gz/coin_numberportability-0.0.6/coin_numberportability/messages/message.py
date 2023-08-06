from coin_numberportability.domain import MessageType


class Message:
    def __init__(self, message, message_type: MessageType):
        self._message = message
        self._message_type = message_type

    def get_message(self):
        return self._message

    def get_message_type(self):
        return self._message_type

    def to_dict(self):
        return {'message': self._message.to_dict()}
