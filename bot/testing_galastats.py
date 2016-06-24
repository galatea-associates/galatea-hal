import unittest
from mock import MagicMock, Mock
from intenthandlers.utils import get_highest_confidence_entity
import intenthandlers.galastats as gs

class TestGalastats(unittest.TestCase):
    def setUp(self):
        pass

    def test_count_galateans(self):
        attrs = {'send_message.return_value': None}
        msg_writer_mock = Mock()
        msg_writer_mock.configure_mock(**attrs)
        event = {'channel': 'dummy channel'}
        wit_entities = "dummy entities"
        get_highest_confidence_entity = MagicMock(return_value=None)  # NOT WORKING AS INTENDED! needs to be fixed
        self.assertEqual(gs.count_galateans(msg_writer_mock, event, wit_entities), None)
        get_highest_confidence_entity = MagicMock(return_value={'value': 'england'})
        self.assertEqual(gs.count_galateans(msg_writer_mock, event, wit_entities), None)
        get_highest_confidence_entity = MagicMock(return_value={'value': 'atlanta'})
        self.assertEqual(gs.count_galateans(msg_writer_mock, event, wit_entities), None)


if __name__ == '__main__':
    unittest.main()