import unittest
import intenthandlers.utils as utils

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_highest_confidence_entity(self):
        sample_entities_dict_1 = {u'randomize_option': [{u'suggested': True, u'confidence': 0.5173704573627974, u'type': u'value', u'value': u'quote'}], u'intent': [{u'confidence': 0.7794858005199589, u'value': u'movie-quote'}]}
        sample_entity_1_1 = u'intent'
        sample_entity_1_2 = u'randomize_option'
        sample_entity_1_3 = u'other'
        self.assertEqual(utils.get_highest_confidence_entity(sample_entities_dict_1, sample_entity_1_1), {u'confidence': 0.7794858005199589, u'value': u'movie-quote'})
        self.assertEqual(utils.get_highest_confidence_entity(sample_entities_dict_1, sample_entity_1_2), None)
        self.assertEqual(utils.get_highest_confidence_entity(sample_entities_dict_1, sample_entity_1_3), None)


if __name__ == '__main__':
    unittest.main()
