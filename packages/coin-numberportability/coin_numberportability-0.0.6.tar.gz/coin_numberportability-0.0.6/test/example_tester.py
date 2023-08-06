import random
import unittest
from collections import namedtuple

from requests import HTTPError

from coin_numberportability.domain import ConfirmationStatus
from coin_numberportability.messages.cancel import CancelBuilder
from coin_numberportability.messages.deactivation import DeactivationBuilder
from coin_numberportability.messages.portingperformed import PortingPerformedBuilder
from coin_numberportability.messages.portingrequest import PortingRequestBuilder
from coin_numberportability.messages.portingrequestanswer import PortingRequestAnswerBuilder
from coin_numberportability.messages.portingrequestanswerdelayed import PortingRequestAnswerDelayedBuilder
from coin_numberportability.receiver import Receiver
from coin_numberportability.sender import Sender
from test.config import TestConfig


class ExamplesTest(unittest.TestCase):
    _sender = Sender(TestConfig)

    def test_porting_request(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_request = (
            PortingRequestBuilder()
            .set_dossierid(dossier_id)
            .set_recipientnetworkoperator('LOADB')
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .add_porting_request_seq()
                .set_number_series('0612345678', '0612345678')
                .finish()
            .add_porting_request_seq()
                .set_number_series('0612345678', '0612345678')
                .add_enum_profiles('PROF1', 'PROF2')
                .finish()
            .set_customerinfo("test", "test bv", "1", "a", "1234AB", "1")
            .build()
        )
        self._sender.send_message(porting_request)

    def test_cancel(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        cancel = CancelBuilder() \
            .set_dossierid(dossier_id) \
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB') \
            .build()
        self._sender.send_message(cancel)

    def test_deactivation(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        deactivation = (
            DeactivationBuilder()
            .set_header(sender_network_operator='LOADA', receiver_network_operator='LOADB')
            .set_dossierid(dossier_id)
            .set_currentnetworkoperator('LOADB')
            .set_originalnetworkoperator('LOADA')
            .add_deactivation_seq()
                .set_number_series('0612345678', '0612345678')
                .finish()
            .build()
        )
        self._sender.send_message(deactivation)

    def test_porting_performed(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_performed = (
            PortingPerformedBuilder()
            .set_header('LOADA', 'LOADB')
            .set_dossierid(dossier_id)
            .set_donornetworkoperator('LOADB')
            .set_recipientnetworkoperator('LOADA')
            .add_porting_performed_seq()
                .set_number_series('0612345678', '0612345678')
                .finish()
            .add_porting_performed_seq()
                .set_number_series('0612345678', '0612345678')
                .add_enum_profiles('PROF1', 'PROF2')
                .finish()
            .build()
        )
        self._sender.send_message(porting_performed)

    def test_porting_request_answer(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_performed_answer = (
            PortingRequestAnswerBuilder()
            .set_header('LOADA', 'LOADB')
            .set_dossierid(dossier_id)
            .set_blocking('N')
            .add_porting_request_answer_seq()
                .set_donornetworkoperator('LOADA')
                .set_donorserviceprovider('LOADA')
                .set_firstpossibledate('20190101120000')
                .set_number_series('0612345678', '0612345678')
                .set_note('This is a note')
                .set_blockingcode('99')
                .finish()
            .add_porting_request_answer_seq()
                .set_donornetworkoperator('LOADA')
                .set_donorserviceprovider('LOADA')
                .set_firstpossibledate('20190101120000')
                .set_number_series('0612345678', '0612345678')
                .set_note('This is a note')
                .set_blockingcode('99')
                .finish()
            .build()
        )
        self._sender.send_message(porting_performed_answer)

    def test_porting_request_answer_delayed(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_request_answer_delayed = (
            PortingRequestAnswerDelayedBuilder()
            .set_header('LOADA', 'LOADA')
            .set_dossierid(dossier_id)
            .set_donornetworkoperator('LOADB')
            .build()
        )
        self._sender.send_message(porting_request_answer_delayed)

    def test_send_error(self):
        dossier_id = self._generate_random_dossier_id('LOADA')
        porting_request_answer_delayed = (
            PortingRequestAnswerDelayedBuilder()
                .set_header('LOADA', 'LOADA')
                .set_dossierid(dossier_id)
                .set_donornetworkoperator('LOADB')
                .build()
        )
        porting_request_answer_delayed._message_type = namedtuple('x', 'value')('false')
        try:
            self._sender.send_message(porting_request_answer_delayed)
        except HTTPError as e:
            print(e)

    def test_receive_message(self):
        TestConfig.consumerName = 'loadtest-loadb'
        TestReceiver(TestConfig).start_stream(confirmation_status=ConfirmationStatus.ALL)

    @staticmethod
    def _generate_random_dossier_id(operator: str):
        random_int = random.randint(10000, 99999)
        return f'{operator}-{random_int}'


class TestReceiver(Receiver):
    _sender = Sender(TestConfig)

    def on_porting_request(self, message_id, message):
        print('porting request')
        self.handle_message(message_id, message)

    def on_porting_request_answer(self, message_id, message):
        print('porting request answer')
        self.handle_message(message_id, message)

    def on_porting_request_answer_delayed(self, message_id, message):
        print('porting request answer delayed')
        self.handle_message(message_id, message)

    def on_porting_performed(self, message_id, message):
        print('porting performed')
        self.handle_message(message_id, message)

    def on_deactivation(self, message_id, message):
        print('deactivation')
        self.handle_message(message_id, message)

    def on_cancel(self, message_id, message):
        print('cancel')
        self.handle_message(message_id, message)

    def on_error_found(self, message_id, message):
        print('error!')
        self.handle_message(message_id, message)

    def handle_message(self, message_id, message):
        print(message)
        self._sender.confirm(message_id)


if __name__ == '__main__':
    unittest.main()
