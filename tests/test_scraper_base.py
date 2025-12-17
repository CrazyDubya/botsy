import unittest
from utils.scraper_base import BaseScraper
from unittest.mock import MagicMock, patch
import os
import shutil

class TestBaseScraper(BaseScraper):
    def scrape(self):
        return [{"title": "test", "data": "value"}]
    def get_available_tools(self):
        return {}

class TestScraperBase(unittest.TestCase):
    def setUp(self):
        self.scraper = TestBaseScraper("test_category")

    def tearDown(self):
        if os.path.exists("data"):
            # Clean up created files but be careful not to delete real data if possible
            # For this test environment, we might just leave it or use a temp dir.
            pass

    def test_init(self):
        self.assertEqual(self.scraper.category, "test_category")
        self.assertIsNotNone(self.scraper.session)

    def test_save_data_json(self):
        data = [{"title": "test", "data": "value"}]
        self.scraper.save_data(data, "test_file")
        self.assertTrue(os.path.exists("data/test_category_test_file.json"))

if __name__ == '__main__':
    unittest.main()
