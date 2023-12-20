from abc import ABC, abstractmethod
from selenium import webdriver
from notifier import EmailNotifier


class AbstractWatcher(ABC):
    """Abstract watcher."""

    @abstractmethod
    def watch(self):
        pass


class AmazonPriceWatcher(AbstractWatcher):
    """Amazon price watcher."""

    _options = webdriver.ChromeOptions()

    def __init__(self, url):
        AmazonPriceWatcher.set_options()
        self.notifier = EmailNotifier()
        self._url = url

    @property
    def options(self):
        return self._options

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

    @classmethod
    def set_options(cls) -> None:
        """Set options to Chrome webdriver."""

        list_options = ['disable-infobars', 'start-maximized',
                        'disable-dev-shm-usage', 'no-sandbox',
                        'disable-gpu', 'headless',
                        'disable-blink-features=AutomationControlled']

        for option in list_options:
            cls._options.add_argument(option)

        cls._options.add_experimental_option('excludeSwitches',
                                             ['enable-automation'])

    def crawl(self):
        """Crawl the price of a product."""

    def watch(self):
        pass


