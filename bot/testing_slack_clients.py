import unittest
from mock import MagicMock, Mock
import slack_clients


class TestSlackClients(unittest.TestCase, slack_clients.SlackClients):
    def setUp(self):
        # Create a mock object to serve as rtm
        mock = Mock(server=Mock(login_data={'self': {'id': 'name'}}))
        self.rtm = mock
        pass

    # Simple test of is_direct_message
    def test_is_direct_message(self):
        sample_channel_id_1 = "C2147483705"
        sample_channel_id_2 = "D1235792374"
        self.assertEqual(slack_clients.is_direct_message(sample_channel_id_1), None)
        self.assertIsNotNone(type(slack_clients.is_direct_message(sample_channel_id_2)))

    # Test of bot_user_id
    def test_bot_user_id(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        self.assertEqual(self.bot_user_id(), 'george')

    # Test of is_message_from_me
    def test_is_message_from_me(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        self.assertEqual(self.is_message_from_me('george'), True)

    # Test of is_bot_mention
    def test_is_bot_mention(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        message_1 = "@george say hello"
        message_2 = "@susan say hello"
        self.assertEqual(self.is_bot_mention(message_1), True)
        self.assertEqual(self.is_bot_mention(message_2), False)

    # Test of remove_mention
    def test_remove_mention(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        message_1 = '<@george> say hello'
        message_2 = '<@george>: say hello'
        self.assertEqual(self.remove_mention(message_1), ' say hello')
        self.assertEqual(self.remove_mention(message_2), ' say hello')

    # Test of send_user_typing_pause
    def test_send_user_typing_pause(self):
        self.rtm.server.send_to_websocket = MagicMock(return_value=None)
        self.assertEqual(self.send_user_typing_pause("dummy channel"), None)

if __name__ == '__main__':
    unittest.main()