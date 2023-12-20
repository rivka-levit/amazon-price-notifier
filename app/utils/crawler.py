from abc import ABC, abstractmethod
from selenium import webdriver


class AbstractCrawler(ABC):
    """Abstract crawler."""

    @abstractmethod
    def crawl(self):
        """Crawl the website and return data."""


class AmazonPriceCrawler (AbstractCrawler):
    """Scrape price from Amazon product page."""

    _options = webdriver.ChromeOptions()

    def __init__(self):
        AmazonPriceCrawler.set_options()

    @property
    def options(self):
        return self._options

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
        """Scrape and return the price of a product."""


if __name__ == '__main__':
    crawler = AmazonPriceCrawler()
    print(crawler.options.arguments)
