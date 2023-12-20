from abc import ABC, abstractmethod
from selenium import webdriver


class AbstractCrawler(ABC):
    """Abstract crawler."""

    @abstractmethod
    def crawl(self):
        """Crawl the website and return data."""


class AmazonPriceCrawler (AbstractCrawler):
    """Scrape price from Amazon product page."""

    def __init__(self):
        self._options = webdriver.ChromeOptions()
        self.set_options()

    @property
    def options(self):
        return self._options

    def set_options(self) -> None:
        """Set options to Chrome webdriver."""

        list_options = ['disable-infobars', 'start-maximized',
                        'disable-dev-shm-usage', 'no-sandbox',
                        'disable-gpu', 'headless',
                        'disable-blink-features=AutomationControlled']

        for option in list_options:
            self._options.add_argument(option)

        self._options.add_experimental_option('excludeSwitches',
                                              ['enable-automation'])

    def crawl(self):
        """Scrape and return the price of a product."""

    @staticmethod
    def clean_data(*args) -> float:
        """Clean data and return float number."""

        if len(args) != 2:
            raise ValueError('Unexpected number of arguments.')

        if any(not isinstance(x, str) for x in args):
            raise ValueError('Unexpected type of arguments.')

        if not args[0].endswith('.'):
            raise ValueError('Unexpected first argument for whole part of price.')

        try:
            price = float(f'{args[0]}{args[1]}')
        except ValueError as err:
            raise ValueError('Can not convert value to float.') from err

        return price
