import logging
import coin_numberportability.config as config


def set_config():
    config.set_base_url('http://localhost:9010')
    config.set_security_config(consumer_name='loadtest-loada', private_key_file='./keys/private-key.pem')
    config.set_logging(level=logging.DEBUG)

