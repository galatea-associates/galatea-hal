import unittest
from mock import MagicMock, Mock
import app


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_main(self):
        # Creating Mock methods and objects to use in testing
        app.bot_manager.BotManager = MagicMock(return_value="dummy bot manager")
        dummy_resourcer = Mock()
        attrs = {'start.return_value': None}
        dummy_resourcer.configure_mock(**attrs)
        app.resourcer.Resourcer = MagicMock(return_value=dummy_resourcer)
        dummy_bot = Mock()
        bot_attrs = {'start.return_value': None}
        dummy_bot.configure_mock(**bot_attrs)
        app.SlackBot = MagicMock(return_value=dummy_bot)

        # Testing with an empty token and a dummy token
        app.os.getenv = MagicMock(return_value="")
        self.assertEqual(app.main(), None)
        app.os.getenv = MagicMock(return_value="dummy token")
        self.assertEqual(app.main(), None)

if __name__ == '__main__':
    unittest.main()