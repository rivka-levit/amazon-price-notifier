import time
from abc import ABC, abstractmethod
from utils.notifier import EmailNotifier, AbstractNotifier
from utils.crawler import AmazonPriceCrawler


class AbstractWatcher(ABC):
    """Abstract watcher."""

    @abstractmethod
    def watch(self):
        pass


class AmazonPriceWatcher(AbstractWatcher):
    """Amazon price watcher."""

    def __init__(self, url, notifiers: list[AbstractNotifier] = None):
        self.crawler = AmazonPriceCrawler()
        self._url = None
        self.url = url
        self._notifiers = set()
        if notifiers:
            for i in notifiers:
                self.add_notifier(i)
        else:
            self.add_notifier(EmailNotifier())

    @property
    def notifiers(self):
        return self._notifiers

    def add_notifier(self, notifier):
        if isinstance(notifier, AbstractNotifier):
            self._notifiers.add(notifier)

    def delete_notifier(self, notifier):
        if notifier in self._notifiers:
            self._notifiers.remove(notifier)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, product_url):
        """Set product url to get the price."""

        if not isinstance(product_url, str):
            raise ValueError("The product url must be a string value.")
        if len(product_url.strip()) == 0:
            raise ValueError("The product url can not be empty.")
        if not product_url.startswith("https://www.amazon.com/"):
            raise ValueError("The product url must start with "
                             "https://www.amazon.com/")

        self._url = product_url

    def watch(self):
        """Watch the product price and notify the observers."""

        currency, sample_price = self.crawler.crawl(self.url)
        price = sample_price

        while price == sample_price:
            time.sleep(900)

            currency, price = self.crawler.crawl(self.url)

            if price != sample_price:
                str_price = f'{currency}{price:.2f}'

                for notifier in self._notifiers:
                    notifier.notify(str_price)
