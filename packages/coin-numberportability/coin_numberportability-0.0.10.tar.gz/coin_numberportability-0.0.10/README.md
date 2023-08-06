# Python SDK
## Introduction
The Python SDK supports secured access to the numberportability API.

For a quickstart follow the steps below:
* [Setup](#setup)
* [Configure Credentials](#cred)
* [Send Messages](#sendm)
* [Consume Messages](#consumption)
* [Error handling](#errorhandling)

## <a name="setup"></a>Setup
### Quickstart Project
- COIN provides a quickstart project, which can be checked out as follows:

    `git clone https://gitlab.com/verenigingcoin-public/number-portability-quickstart.git`

Go to the subfolder python-quickstart. All the required python packages are defined in the Pipfile. To initialize the right environment:
- pipenv shell
- pipenv install

## <a name="cred"></a>Configure Credentials
For secure access various credentials are required. 
- How to configure credentials see [the introduction section](../README.md)
- As a summary you will need:
    - Consumer name 
    - `private-key.pem` file
    - `sharedkey.encrypted` (encrypted (by public key) HMAC secret)  file

Configure these setting at the bottom of the quickstart.py file: 
  
```python
if __name__ == '__main__':
    config.set_base_url('https://test-api.coin.nl')
    config.set_security_config(consumer_name='<your-consumer-name>', private_key_file='<path-to/private-key.pem>', encrypted_shared_key_file='<path-to/sharedkey.encrypted>')

    sender = QuickstartSender()
    sender.porting_request()

    receiver = QuickstartReceiver()
    receiver.start_stream()
```
See the documentation on the [Vereniging COIN GitLab](https://gitlab.com/verenigingcoin-public/number-portability-sdk) how to generate the required credentials for the `private_key_file` and `encrypted_shared_key_file` files in `set_security_config`.

## <a name="sendm"></a>Send Messages
For sending messages the SDK provides various message builders to create payloads. After the message is created it can be send.

### <a name="senderex"></a>Create and send a Message
To send a message, build a message and simply call the `send()` function of the `message`.

Example:
```python
from coin_numberportability.messages.portingrequest import PortingRequestBuilder


dossier_id = "TEST-1234"

porting_request = (
	PortingRequestBuilder()
		.set_dossier_id(dossier_id)
		.set_recipient_network_operator('TESTB')
		.set_header(sender_network_operator='TESTA', receiver_network_operator='TESTB')
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
porting_request.send()
```

When successful (HTTP 200), the `send()` function returns a `MessageResponse` object:
```python
class MessageResponse:
    transaction_id: str
``` 
When unsuccessful (HTTP != 200), the `send()` function will throw an `requests.HTTPError`.
When applicable, this error contains the error code and description returned by the API.

### <a name="senderexcat"></a>Sender Examples Catalogue
In the [quickstart project](`https://gitlab.com/verenigingcoin-public/number-portability-quickstart/tree/master/python-quickstart`) you can find the following sender examples: 
- `PortingRequestExample`
- `PortingRequestAnswerExample`
- `PortingRequestAnswerDelayedExample`
- `PortingPerformedExample`
- `CancelExample`
- `DeactivationExample`
- `InvalidMessage`

## <a name="consumption"></a>Consume Messages
### <a name="listener"></a>Create Message Listener
For message consumption the numberportability API makes use of http's [ServerSentEvents](https://en.wikipedia.org/wiki/Server-sent_events).
The SDK provides a receiver class that takes care of messages incoming from the event stream. This class also provides the possibility to act upon the different porting messages that are streamed.
To use the receiver, you will have to extend it and implement the abstract methods:

Example:
```python
from coin_numberportability.receiver import Receiver
from coin_numberportability.sender import confirm


class MyReceiver(Receiver):
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
        confirm(message_id)
```

### <a name="consumer"></a>Start consuming Messages 

By default the Receiver consumes <strong>all</strong> <strong>Unconfirmed</strong> messages. 

Here an example:
```python
MyReceiver().start_stream()
```

### <a name="filter"></a>Consume specific messages using filters

The `NumberPortabilityMessageConsumer` provides various ways / filters how messages can be consumed. The filters are:
- `MessageType`: All possible message types including errors.
- ConfirmationStatus: 
    - `ConfirmationStatus.UNCONFIRMED`: consumed all unconfirmed messages. Upon (re)-connection all unconfirmed messages are served.
    - `ConfirmationStatus.ALL`: consumes confirmed and unconfirmed messages. <strong>Note:</strong> this filter enables the consumption of the *whole message history*. Therefore, this filter can best be used in conjunction with the `offset`. 
- `offset`: starts consuming messages based on the given `message-id` offset. When using `ConfirmationStatus.UNCONFIRMED` the `offset` is (in most cases) of no use. Using the `ConfirmationStatus.ALL` filter it can be valuable. <strong>Note:</strong> it is the responsibility of the client to keep track of the `offset`.

#### <a name="ex1"></a>Consumer Filter Example 1: filter on MessageTypes
```python
# only listen for portingperformed mesages
receiver.start_stream(confirmation_status = ConfirmationStatus.UNCONFIRMED, message_types = [MessageType.PORTING_PERFORMED_V1]) 
```

#### <a name="ex2"></a>Consumer Filter Example 2: filter on offset
```
# get all messages from offset 1234
receiver.start_stream(offset = 1234, confirmation_status = ConfirmationStatus.ALL) 
```
The `message`-input variable is a `namedtuple`, so the `message` properties can be accessed object-wise:
```python
# example
networkoperator = message.header.receiver.networkoperator
dossierid = message.body.portingrequest.dossierid
``` 
Property-names are equal to the property-names in the event stream JSON.
See the [Swagger-File](https://test-api.coin.nl/docs/number-portability/v1/swagger.json) for the JSON-definitions of the different messages. 


#### <a name="errorhandling"></a>Handle Errors
When unsuccessful (HTTP != 200), the `send()` function will throw an `requests.HTTPError`.
When applicable, this error contains the error code and description returned by the API.


