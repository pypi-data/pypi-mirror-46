import logging


class Config:
    def __init__(self):
        # Endpoint config
        # ---------------
        self._base_url = ""
        self._api_url = ""
        self._sse_url = ""
        self.baseUrl = 'https://test-api.coin.nl'

        # Security config
        # ---------------
        # Provide the following security configuration for the python client to work:
        # - Name of the consumer as configured in https://test-portal.coin.nl/iam#/
        self._consumer_name = '<<consumer>>'
        # - Path to private key file
        self._private_key_file = './keys/private-key.pem'
        # - Path to encrypted HMAC secret for given consumer as copied from https://test-portal.coin.nl/iam#/
        self._encrypted_shared_key_file = './keys/sharedkey.encrypted'

    @property
    def baseUrl(self):
        return self._base_url

    @baseUrl.setter
    def baseUrl(self, url: str):
        self._base_url = url
        self._api_url = f'{url}/number-portability/v1/dossiers'
        self._sse_url = f'{self._api_url}/events'

    @property
    def apiUrl(self):
        return self._api_url

    @property
    def sseUrl(self):
        return self._sse_url

    @property
    def consumerName(self):
        return self._consumer_name

    @consumerName.setter
    def consumerName(self, consumer_name):
        self._consumer_name = consumer_name

    @property
    def privateKeyFile(self):
        return self._private_key_file

    @privateKeyFile.setter
    def privateKeyFile(self, filename):
        self._private_key_file = filename

    @property
    def encryptedSharedKeyFile(self):
        return self._encrypted_shared_key_file

    @encryptedSharedKeyFile.setter
    def encryptedSharedKeyFile(self, filename):
        self._encrypted_shared_key_file = filename


config = Config()
_format = '%(asctime)s - %(name)-8s - %(levelname)s - %(message)s'


def set_base_url(url=config.baseUrl):
    config.baseUrl = url


def set_security_config(consumer_name=config.consumerName, private_key_file=config.privateKeyFile, encrypted_shared_key_file=config.encryptedSharedKeyFile):
    config.consumerName = consumer_name
    config.privateKeyFile = private_key_file
    config.encryptedSharedKeyFile = encrypted_shared_key_file


def set_logging(format=_format, level=logging.ERROR):
    logging.basicConfig(format=format, level=level)
