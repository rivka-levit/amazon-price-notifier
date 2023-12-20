"""
Tests for crawler.
"""

from unittest import TestCase

from utils.crawler import AmazonPriceCrawler


class TestCrawler(TestCase):
    """Tests for crawler"""

    def setUp(self) -> None:
        self.crawler = AmazonPriceCrawler()

    def test_default_options_set(self):
        """Test default options were set for crawler"""

        expected_options = ['disable-infobars', 'start-maximized',
                            'disable-dev-shm-usage', 'no-sandbox',
                            'disable-gpu', 'headless',
                            'disable-blink-features=AutomationControlled']

        self.assertEqual(self.crawler.options.arguments, expected_options)
