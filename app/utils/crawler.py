from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from amazoncaptcha import AmazonCaptcha  # noqa

import time


class AbstractCrawler(ABC):
    """Abstract crawler."""

    @abstractmethod
    def crawl(self, url: str):
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

    def crawl(self, url: str) -> tuple:
        """Scrape and return the price of a product."""

        driver = webdriver.Remote(
            command_executor='http://chrome:4444',
            options=self.options
        )
        driver.get(url)
        # print(driver.page_source)

        try:
            input_captcha = driver.find_element(By.ID, 'captchacharacters')

            captcha = AmazonCaptcha.fromdriver(driver)
            solution = captcha.solve()
            print(solution)
            input_captcha.send_keys(solution)
            button = driver.find_element(By.LINK_TEXT, 'Continue shopping')

            button.click()
            driver.get(url)
        except NoSuchElementException:
            pass

        price_symbol = driver.find_element(
            By.XPATH,
            '//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-symbol"]'
        ).text

        price_whole = driver.find_element(
            By.XPATH,
            '//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"]'
        ).text

        price_fraction = driver.find_element(
            By.XPATH,
            '//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-fraction"]'
        ).text

        driver.quit()

        return price_symbol, self.clean_data(price_whole, price_fraction)

    @staticmethod
    def clean_data(whole: str, fract: str) -> float:
        """Clean data and return float number."""

        if any(not isinstance(x, str) for x in (whole, fract)):
            raise ValueError('Unexpected type of arguments.')

        try:
            price = float(f'{whole}.{fract}')
        except ValueError as err:
            raise ValueError('Can not convert value to float.') from err

        return price
