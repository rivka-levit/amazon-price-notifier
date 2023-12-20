"""
Test observing the price and sending notification.
"""

from unittest import TestCase

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

        ntf2 = EmailNotifier()
        self.watcher.add_notifier(ntf2)

        self.assertEqual(len(self.watcher.notifiers), 2)

    def test_delete_notifier_success(self):
        """Test deleting a notifier successfully."""

        nfr1 = EmailNotifier()
        nfr2 = EmailNotifier()
        params = {'notifiers': [nfr1, nfr2]}
        wtr = create_watcher(**params)

        wtr.delete_notifier(nfr1)

        self.assertEqual(len(wtr.notifiers), 1)
        self.assertEqual(*wtr.notifiers, nfr2)
