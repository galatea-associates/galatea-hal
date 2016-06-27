import unittest
from mock import MagicMock, Mock
from slack_bot import SlackBot

class TestSlackBot(unittest.TestCase):
    def setUp(self):
        pass

    # Tests __init__ by passing in a dummy set of clients, and then
    # ensuring that those clients are found in slackbot.clients
    def test_init(self):
        mock_slack_clients = MagicMock(return_value="dummy clients")
        slackbot = SlackBot("token", mock_slack_clients)
        self.assertEqual(slackbot.clients, "dummy clients")

    def test_start(self):
        # A large set of mocks required to make sure that this test tests start, not
        # any other function
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

        # Ensure that start completes without error
        self.assertEqual(slackbot.start(resource, mock_messenger, mock_rtm), None)

    def test_stop(self):
        # Test to ensure that the keep_running variable is properly set to false
        # When stop is called, and that stop returns without error
        mock_slack_clients = MagicMock(return_value="dummy clients")
        slackbot = SlackBot("token", mock_slack_clients)
        self.assertEqual(slackbot.stop("dummy resource"), None)
        self.assertEqual(slackbot.keep_running, False)

if __name__ == '__main__':
    unittest.main()