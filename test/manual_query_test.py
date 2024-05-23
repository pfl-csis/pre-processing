import unittest
from testSettings import *
from services.alertEnrichment.manual_query_dande import manual_ioc_query

class ManualQueryTest(unittest.TestCase, TestSettings):

    def setUp(self):
        self.iocs = {
            "8.8.8.8": "IP",
            "google.com": "Domain",
            "8271c6da32ce3f4f8b7ad68e1cec3cde4716c9d7": "hash"
        }

    def test_manual_ioc_query(self):
        result = manual_ioc_query(self.iocs)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)
        for ioc in self.iocs.keys():
            self.assertIn(ioc, result)

    def tearDown(self) -> None:
        self.iocs = None
        return super().tearDown()