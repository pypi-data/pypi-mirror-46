from enum import Enum


class ConfirmationStatus(Enum):
    CONFIRMED = "Confirmed"
    ALL = "All"


class MessageType(Enum):
    PORTING_REQUEST_V1 = "portingrequest"
    PORTING_REQUEST_ANSWER_V1 = "portingrequestanswer"
    PORTING_PERFORMED_V1 = "portingperformed"
    PORTING_REQUEST_ANSWER_DELAYED_V1 = "pradelayed"
    CANCEL_V1 = "cancel"
    DEACTIVATION_V1 = "deactivation"
    CONFIRMATION_V1 = "confirmations"
    ERROR_FOUND_V1 = "errorfound"
    _VERSION_SUFFIX_V1 = "-v1"

    def get_event_type(self):
        return f'{self.value}{self._VERSION_SUFFIX_V1.value}'


class Config:
    # Endpoint config
    # ---------------
    baseUrl = 'https://test-api.coin.nl'
    apiUrl = f'{baseUrl}/number-portability/v1/dossiers'
    sseUrl = f'{apiUrl}/events'

    # Security config
    # ---------------
    # Provide the following security configuration for the python client to work:
    # - Name of the consumer as configured in https://dev-portal.coin.nl/iam#/
    consumerName = '<<consumer>>'
    # - Path to private key file
    privateKeyFile='./keys/private-key.pem'
    # - Path to encrypted HMAC secret for given consumer as copied from https://dev-portal.coin.nl/iam#/
    encryptedSharedKeyFile='./keys/sharedkey.encrypted'

