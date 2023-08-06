CRDB REST Python SDK
=========================

Python SDK to access VereningingCOIN's numberportability for telecom providers in The Netherlands.

Setup
=========================

Configuration can be set in `config.py`.

##### Configuration
Extend the `Config` class to set your configuration.
The `Sender` and `Receiver` classes require this object to properly send and receive messages. 
```python
from coin_numberportability.domain import Config


class MyConfig(Config):
	# This is the default configuration coming from Config
	baseUrl = 'https://test-api.coin.nl'
	apiUrl = f'{baseUrl}/number-portability/v1/dossiers'
	sseUrl = f'{apiUrl}/events'
	consumerName = '<<consumer>>'
	privateKeyFile='./keys/private-key.pem'
	encryptedSharedKeyFile='./keys/sharedkey.encrypted'
```

##### Sending a message
The SDK contains provides the developer with Builder classes.
With these Builder classes the developer can construct porting messages, set properties on these classes and and other constructs to the messages.
Builder classes exist for the following messages:
- PortingRequest Message
- PortingRequestAnswer Message
- PortingRequestAnswerDelayed Message
- PortingPerformed Message
- Deactivation Message
- Cancel Message

To send the message, use the `send_message` function of the `Sender` class.

Example:
```python
from coin_numberportability.messages.portingrequest import PortingRequestBuilder
from coin_numberportability.sender import Sender


sender = Sender(MyConfig)
dossier_id = "TEST-1234"

porting_request = (
	PortingRequestBuilder()
		.set_dossier_id(dossier_id)
		.set_recipient_network_operator('LOADB')
		.set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
		.add_porting_request_seq()
			.set_number_series('0612345678', '0612345678')
			.finish()
		.add_porting_request_seq()
			.set_number_series('0612345678', '0612345678')
			.add_enum_profiles('PROF1', 'PROF2')
			.finish()
		.set_customer_info("test", "test bv", "1", "a", "1234AB", "1")
		.build()
	)
sender.send_message(porting_request)
```

When successful (HTTP 200), the `send_message()` function returns a `MessageResponse` object:
```python
class MessageResponse:
    transaction_id: str
``` 
When unsuccessful (HTTP != 200), the `send_message()` function will throw an `requests.HTTPError`.
When applicable, this error contains the error code and description returned by the API.

##### Receiving a message
The SDK provides a receiver class that takes care of messages incoming from the event stream.
This class also provides the possibility to act upon the different porting messages that are streamed.
To use the receiver, you will have to extend it and implement the absract methods:

Example:
```python
from coin_numberportability.receiver import Receiver
from coin_numberportability.sender import confirm


class MyReceiver(Receiver):
	_sender = Sender(MyConfig)
	
    # mandatory function
    def on_porting_request(self, message_id, message):
        print('porting request')
        self.handle_message(message_id, message)

    # mandatory function
    def on_porting_request_answer(self, message_id, message):
        print('porting request answer')
        self.handle_message(message_id, message)

    # mandatory function
    def on_porting_request_answer_delayed(self, message_id, message):
        print('porting request answer delayed')
        self.handle_message(message_id, message)

    # mandatory function
    def on_porting_performed(self, message_id, message):
        print('porting performed')
        self.handle_message(message_id, message)

    # mandatory function
    def on_deactivation(self, message_id, message):
        print('deactivation')
        self.handle_message(message_id, message)

    # mandatory function
    def on_cancel(self, message_id, message):
        print('cancel')
        self.handle_message(message_id, message)

    # mandatory function
    def on_error_found(self, message_id, message):
        print('error!')
        self.handle_message(message_id, message)

    def handle_message(self, message_id, message):
        print(message)
        self._sender.confirm(message_id)

MyReceiver(MyConfig).start_stream()
```

The `message`-input variable is a `namedtuple`, so the `message` properties can be accessed object-wise:
```python
# example
networkoperator = message.header.receiver.networkoperator
dossierid = message.body.portingrequest.dossierid
``` 
Property-names are equal to the property-names in the event stream JSON.
See the [Swagger-File](https://dev-api.coin.nl/docs/number-portability/v1/swagger.json) for the JSON-definitions of the different messages. 
