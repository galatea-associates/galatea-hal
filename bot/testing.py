import types
import unittest
import os

from hypothesis import given
from hypothesis.strategies import text
from schema import Schema

from event_handler import RtmEventHandler, intents
from messenger import Messenger
from slack_clients import SlackClients



class TestEventHandler(unittest.TestCase, RtmEventHandler):

    def setUp(self):
        slack_token = os.getenv("SLACK_TOKEN", "")
        self.clients = SlackClients(slack_token)
        self.msg_writer = Messenger(self.clients)
        self.handler = RtmEventHandler(self.clients, self.msg_writer)
        pass

    # test to ensure intents is properly formed
    def test_validate_intents(self):
        # schema returns passed data if data is valid
        schema = Schema({
            'func': types.FunctionType,
            'sample': str
        })
        for c in intents:
            self.assertEqual(schema.validate(intents[c]), intents[c])

    @given(sample_message=text())
    def test_handle_message(self, sample_message):
        test_message = {'type': 'message', 'channel': 'C2147483705', 'user': 'U2147483697', 'text': sample_message,
                        'ts': '1355517523.000005'}

        assert self.handler._handle_message(test_message) is None  # not good yet

if __name__ == '__main__':
    unittest.main()