import unittest
from mock import MagicMock, Mock
from slack_bot import SlackBot

class TestSlackBot(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        mock_slack_clients = MagicMock(return_value="dummy clients")
        slackbot = SlackBot("token", mock_slack_clients)
        self.assertEqual(slackbot.clients, "dummy clients")

    def test_start(self):
        # Does not currently cover exception in the event read loop
        resource = {
            'resource': {
                'SlackBotAccessToken': 'token'
            }
        }
        mock_messenger = MagicMock(return_value="dummy messenger")
        mock_event_handler = Mock()
        attrs = {'handle.return_value': "dummy return"}
        mock_event_handler.configure_mock(**attrs)
        mock_rtm = MagicMock(return_value=mock_event_handler)
        mock_slack_clients = MagicMock(return_value="dummy clients")
        slackbot = SlackBot("token", mock_slack_clients)
        slackbot.clients = Mock(rtm=Mock(rtm_connect=None, rtm_read=None, server=Mock(username=None, login_data={'team':{'name': None}}, domain=None)))

        slackbot.clients.rtm.rtm_connect = MagicMock(return_value=True)
        slackbot.clients.rtm.server.username = "dummy username"
        slackbot.clients.rtm.server.login_data['team']['name'] = "dummy team name"
        slackbot.clients.rtm.server.domain = "dummy domain"
        slackbot.clients.rtm.rtm_read = MagicMock(return_value=['event1', 'event2', 'event3'])
        self.assertEqual(slackbot.start(resource, mock_messenger, mock_rtm), None)

    def test_stop(self):
        mock_slack_clients = MagicMock(return_value="dummy clients")
        slackbot = SlackBot("token", mock_slack_clients)
        self.assertEqual(slackbot.stop("dummy resource"), None)
        self.assertEqual(slackbot.keep_running, False)

if __name__ == '__main__':
    unittest.main()