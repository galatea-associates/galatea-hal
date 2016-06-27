import unittest
from mock import MagicMock, Mock
import intenthandlers.galastats as gs


class TestGalastats(unittest.TestCase):
    def setUp(self):
        pass

    # Test of Count galateans
    def test_count_galateans(self):
        # Create a set of dummy objects to use in count galateans
        attrs = {'send_message.return_value': None}
        msg_writer_mock = Mock()
        msg_writer_mock.configure_mock(**attrs)
        event = {'channel': 'dummy channel'}
        wit_entities = "dummy entities"

        # Test no location, valid location, and invalid location
        get_highest_confidence_entity = MagicMock(return_value=None)
        self.assertEqual(gs.count_galateans(msg_writer_mock, event, wit_entities, get_highest_confidence_entity), None)
        get_highest_confidence_entity = MagicMock(return_value={'value': 'england'})
        self.assertEqual(gs.count_galateans(msg_writer_mock, event, wit_entities, get_highest_confidence_entity), None)
        get_highest_confidence_entity = MagicMock(return_value={'value': 'atlanta'})
        self.assertEqual(gs.count_galateans(msg_writer_mock, event, wit_entities, get_highest_confidence_entity), None)


if __name__ == '__main__':
    unittest.main()