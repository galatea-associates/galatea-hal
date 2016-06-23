import unittest
from mock import MagicMock, Mock
import slack_clients


class TestSlackClients(unittest.TestCase, slack_clients.SlackClients):
    def setUp(self):
        mock = Mock(server=Mock(login_data={'self': {'id': 'name'}}))
        self.rtm = mock
        pass

    def test_is_direct_message(self):
        sample_channel_id_1 = "C2147483705"
        sample_channel_id_2 = "D1235792374"
        self.assertEqual(slack_clients.is_direct_message(sample_channel_id_1), None)
        self.assertIsNotNone(type(slack_clients.is_direct_message(sample_channel_id_2)))

    def test_bot_user_id(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        self.assertEqual(self.bot_user_id(), 'george')

    def test_is_message_from_me(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        self.assertEqual(self.is_message_from_me('george'), True)

    def test_is_bot_mention(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        message_1 = "@george say hello"
        message_2 = "@susan say hello"
        self.assertEqual(self.is_bot_mention(message_1), True)
        self.assertEqual(self.is_bot_mention(message_2), False)

    def test_remove_mention(self):
        self.rtm.server.login_data['self']['id'] = 'george'
        message_1 = '<@george> say hello'
        message_2 = '<@george>: say hello'
        self.assertEqual(self.remove_mention(message_1), ' say hello')
        self.assertEqual(self.remove_mention(message_2), ' say hello')

    # NOTE: NO CURRENT TEST FOR send_user_typing_pause


if __name__ == '__main__':
    unittest.main()