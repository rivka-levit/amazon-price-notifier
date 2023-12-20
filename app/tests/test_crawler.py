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

    def test_clean_data_return_float(self):
        """Test clean_data method returns a float number."""

        data = ('16.', '35')
        expected_result = float(f'{data[0]}{data[1]}')

        result = self.crawler.clean_data(*data)

        self.assertIsInstance(result, float)
        self.assertEqual(result, expected_result)

    def test_clean_data_unexpected_arg_error(self):
        """Test clean_data raise error with not enough arguments."""

        data = '16'

        with self.assertRaises(ValueError):
            self.crawler.clean_data(data)

    def test_clean_data_unexpected_type_arg_error(self):
        """Test clean_data raise error with not string type argument."""

        data = ('16.', 35)

        with self.assertRaises(ValueError):
            self.crawler.clean_data(data)

    def test_clean_data_unexpected_first_value_error(self):
        """Test clean_data raise error with wrong first argument."""

        data = ('1', '6')

        with self.assertRaises(ValueError):
            self.crawler.clean_data(data)

    def test_clean_data_convert_float_error(self):
        """Test clean_data raise error when converting to float a wrong value."""

        data = ('rrf', 'asdf')

        with self.assertRaises(ValueError):
            self.crawler.clean_data(data)
