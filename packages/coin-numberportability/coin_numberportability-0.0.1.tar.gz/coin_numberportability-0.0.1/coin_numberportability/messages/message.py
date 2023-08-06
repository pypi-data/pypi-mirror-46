from coin_numberportability.domain import MessageType
import numberportability.sender as sender


class Message:
    def __init__(self, message, message_type: MessageType):
        self._message = message
        self._message_type = message_type

    def get_message(self):
        return self._message

    def get_message_type(self):
        return self._message_type

    def send(self):
        return sender.send_message(self)

    def to_dict(self):
        return {'message': self._message.to_dict()}
