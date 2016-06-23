import unittest
import intenthandlers.misc as misc
import logging

from messenger import Messenger
from mock import MagicMock
from wit import Wit
from slack_clients import SlackClients


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

class TestMisc(unittest.TestCase):
    def setUp(self):
        self.clients = SlackClients('na')
        self.logger = logging.getLogger(__name__)
        self.actions = {
            'say': say,
            'error': error,
            'merge': merge,
        }
        self.wit_client = Wit("na", self.actions, self.logger)
        self.msg_writer = Messenger(self.clients)
        self.msg_writer.send_message = MagicMock(return_value=None)
        pass

    def test_say_quote(self):
        event = {'user': 'dummy_user', 'channel': 'dummy_channel'}
        wit_entities = None
        self.assertEqual(misc.say_quote(self.msg_writer, event, wit_entities), None)

    def test_randomize_options(self):
        event = {'user': 'dummy_user', 'channel': 'dummy_channel'}
        wit_entities = {'randomize_option': [{'value': 'cookies'}, {'value': 'cake'}]}
        self.assertEqual(misc.randomize_options(self.msg_writer, event, wit_entities), None)

    def test_flip_coin(self):
        event = {'user': 'dummy_user', 'channel': 'dummy_channel'}
        wit_entities = None
        self.assertEqual(misc.flip_coin(self.msg_writer, event, wit_entities), None)

if __name__ == '__main__':
    unittest.main()
