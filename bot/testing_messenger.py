import unittest
import logging

from mock import MagicMock, Mock
from messenger import Messenger

logger = logging.getLogger(__name__)

class TestMessenger(unittest.TestCase, Messenger):
    def setUp(self):
        pass

    def test_send_message(self):
        logger.debug = MagicMock(return_value=None)
        self.clients = Mock(rtm=Mock(server=Mock(channels=Mock(find=Mock()))))
        self.clients.send_message = MagicMock(return_value=None)
        self.assertEqual(self.send_message("dummy channel", "dummy message"), None)

    def test_write_prompt(self):
        dummy_handlers = {
            "item 1": ("junk", "sample 1"),
            "item 2": ("junk", "sample 2"),
            "item 3": ("junk", "sample 3")
        }
        self.send_message = MagicMock(return_value=None)
        self.assertEqual(self.write_prompt("dummy channel", dummy_handlers), None)

    def test_say_hi(self):
        self.send_message = MagicMock(return_value=None)
        self.assertEqual(self.say_hi("dummy channel", "dummy user"), None)

    def test_write_error(self):
        self.send_message = MagicMock(return_value=None)
        self.assertEqual(self.write_error("dummy channel", "dummy error message"), None)

    # NO test written for demo_attachment as it is a dummy function

if __name__ == '__main__':
    unittest.main()