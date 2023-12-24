"""
Test observing the price and sending notification.
"""

from unittest import TestCase
from unittest.mock import patch

from utils.watcher import AmazonPriceWatcher
from utils.crawler import AmazonPriceCrawler
from utils.notifier import EmailNotifier


def create_watcher(**params):
    """Create an AmazonPriceWatcher with additional parameters if passed."""

    defaults = {
        'url': ('https://www.amazon.com/PF-WaterWorks-PF0989-Disposal-'
                'Installation/dp/B078H38Q1M/')
    }
    defaults.update(**params)

    return AmazonPriceWatcher(**defaults)


class TestAmazonWatcher(TestCase):

    def setUp(self):
        self.watcher = create_watcher()

    def test_default_settings(self):
        """Test the default settings."""

        self.assertIsInstance(self.watcher.crawler, AmazonPriceCrawler)
        for ntf in self.watcher.notifiers:
            self.assertIsInstance(ntf, EmailNotifier)

    def test_add_notifier_success(self):
        """Test adding a notifier successfully."""

        ntf2 = EmailNotifier(receiver='some@example.com')
        self.watcher.add_notifier(ntf2)

        self.assertEqual(len(self.watcher.notifiers), 2)

    def test_delete_notifier_success(self):
        """Test deleting a notifier successfully."""

        wtr = create_watcher()

        wtr.delete_notifier(*self.watcher.notifiers)

        self.assertEqual(len(wtr.notifiers), 0)

    def test_set_url_success(self):
        """Test create a watcher with correct url successfully."""

        url = ('https://www.amazon.com/Amazon-Essentials-Womens-Surplice-X-'
               'Large/dp/B097K8N1SC/ref=sr_1_5?_encoding=UTF8&content-id='
               'amzn1.sym.b0c3902d-ae70-4b80-8f54-4d0a3246745a&crid=Y67PJX929'
               'LXO&keywords=Dresses&pd_rd_r=a6e6eb6c-07bf-4ea7-8c0f-dadb492a'
               'ecef&pd_rd_w=B3YIb&pd_rd_wg=rSnk8&pf_rd_p=b0c3902d-ae70-4b80-'
               '8f54-4d0a3246745a&pf_rd_r=S85JJC1JNM45G95A4JYX&qid=1703350904'
               '&refinements=p_36%3A-3000&rnid=2661611011&sprefix=dresses%2'
               'Caps%2C149&sr=8-5&th=1&psc=1')

        wtr = create_watcher(url=url)

        self.assertEqual(wtr.url, url)

    def test_set_wrong_url_fail(self):
        """Test set a wrong url raises an error."""

        non_string_url = 357
        empty_url = ''
        non_amazon_url = 'https://www.udemy.com'

        with self.assertRaisesRegex(
                ValueError,
                r'The product url must be a string value.'
        ):
            create_watcher(url=non_string_url)

        with self.assertRaisesRegex(
                ValueError,
                r'The product url can not be empty.'
        ):
            create_watcher(url=empty_url)

        with self.assertRaisesRegex(
                ValueError,
                r'The product url must start with https://www.amazon.com/'
        ):
            create_watcher(url=non_amazon_url)

    @patch('time.sleep')
    @patch('utils.notifier.EmailNotifier.notify')
    @patch('utils.crawler.AmazonPriceCrawler.crawl')
    def test_watch_price_change_success(self,
                                        patched_crawl,
                                        patched_notify,
                                        patched_sleep):
        """Test watch price change and call notify."""

        patched_crawl.side_effect = [('$', 16.63)] * 3 + [('$', 15.52)]

        self.watcher.watch()

        self.assertEqual(patched_crawl.call_count, 4)
        self.assertEqual(patched_notify.call_count, 1)
