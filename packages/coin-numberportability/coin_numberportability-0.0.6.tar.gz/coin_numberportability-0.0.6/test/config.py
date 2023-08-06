from coin_numberportability.domain import Config


class TestConfig(Config):
    baseUrl = 'http://localhost:9010'
    apiUrl = f'{baseUrl}/number-portability/v1/dossiers'
    sseUrl = f'{apiUrl}/events'

    consumerName = 'loadtest-loada'
    privateKeyFile='./keys/private-key.pem'
    encryptedSharedKeyFile='./keys/sharedkey.encrypted'

