import unittest
from pypydata.list import PypyData


class TestList(unittest.TestCase):
    def test_scraping(self):
        self.assertTrue(PypyData.scraping())