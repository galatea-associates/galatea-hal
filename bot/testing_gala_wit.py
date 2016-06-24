import unittest
import gala_wit
import os
import logging
from mock import MagicMock


logging.disable(logging.CRITICAL)

class TestGalaWit(unittest.TestCase):
    def setUp(self):
        pass

    # Test galawit initialization
    def test_init(self):
        os.getenv = MagicMock(return_value="")
        Wit = MagicMock(return_value=None)
        gw = gala_wit.GalaWit(Wit)
        self.assertEqual(gw.wit_client, None)

    # Test interpret
    def test_interpret(self):
        gw = gala_wit.GalaWit()
        gw.wit_client.message = MagicMock(return_value="test1")
        self.assertEqual(gw.interpret("dummy message"), 'test1')

if __name__ == '__main__':
    unittest.main()