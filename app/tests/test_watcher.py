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

        ntf2 = EmailNotifier(receiver='some@example.com')
        self.watcher.add_notifier(ntf2)

        self.assertEqual(len(self.watcher.notifiers), 2)

    def test_delete_notifier_success(self):
        """Test deleting a notifier successfully."""

        wtr = create_watcher()

        wtr.delete_notifier(*self.watcher.notifiers)

        self.assertEqual(len(wtr.notifiers), 0)
