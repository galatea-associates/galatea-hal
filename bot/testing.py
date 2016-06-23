import logging
import types
import unittest

from hypothesis import given, settings, Verbosity
from hypothesis.strategies import text
from schema import Schema
from mock import MagicMock
from wit import Wit
from messenger import Messenger

from event_handler import RtmEventHandler, intents
from messenger import Messenger
from slack_clients import SlackClients

class Dummy:
    def __init__(self, msg):
        self.msg = msg

    def strip(self):
        return self.msg


def merge(session_id, context, entities, msg):
    # Stub implementation
    return context


def say(session_id, context, msg):
    # Stub implementation
    raise RuntimeError("Should not have been called. Session: {}. Msg: {}. Context: {}".format(session_id,
                                                                                               msg, context))


def error(session_id, context, e):
    # Stub implementation
    raise RuntimeError("Should not have been called. Session: {}. Err   : {}. Context: {}".format(session_id, str(e),
                                                                                                  context))


class TestEventHandler(unittest.TestCase, RtmEventHandler):
    def setUp(self):
        self.clients = SlackClients('na');
        self.logger = logging.getLogger(__name__)
        self.actions = {
            'say': say,
            'error': error,
            'merge': merge,
        }
        self.wit_client = Wit("na", self.actions, self.logger)
        self.msg_writer = Messenger(self.clients)
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

    def test_handle_message(self):
        test_message = {'type': 'message', 'channel': 'dummy_channel', 'user': 'dummy_user', 'text': 'say quote',
                        'ts': '1355517523.000005'}
        self.clients.is_message_from_me = MagicMock(return_value=False)
        self.clients.is_bot_mention = MagicMock(return_value=True)
        self.clients.remove_mention = lambda x: Dummy(x)
        self.wit_client.interpret = MagicMock(return_value={u'entities': {u'randomize_option': [{u'suggested': True, u'confidence': 0.5173704573627974, u'type': u'value', u'value': u'quote'}], u'intent': [{u'confidence': 0.7794858005199589, u'value': u'movie-quote'}]}, u'msg_id': u'89b1ea5b-8844-4106-bfb6-642cd7a48b97', u'_text': u'say quote'})
        self.msg_writer.write_prompt = MagicMock(return_value=None)
        self.msg_writer.send_message = MagicMock(return_value=None)
        self.assertEqual(self._handle_message(test_message), None)

    def test_handle(self):
        event = {'type': 'channel_joined', 'channel': 'dummy_channel'}
        self.assertEqual(self.handle(event), None)
        event = {'type': 'group_joined', 'channel': 'dummy_channel'}
        self.assertEqual(self.handle(event), None)
        event = {'type': 'error'}
        self.assertEqual(self.handle(event), None)
        event = {'type': 'message', 'channel': 'dummy_channel', 'user': 'dummy_user', 'text': 'say quote',
                        'ts': '1355517523.000005'}
        self.assertEqual(self.handle(event), None)

    """
    @given(sample_message=text(min_size=1))
    @settings(verbosity=Verbosity.verbose)
    def test_handle_message(self, sample_message):
        test_message = {'type': 'message', 'channel': 'NA', 'user': 'NA', 'text': sample_message,
                        'ts': '1355517523.000005'}

        assert self.handler._handle_message(test_message) is None  # not good yet
    """

if __name__ == '__main__':
    unittest.main()
