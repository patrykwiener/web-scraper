"""This module contains scraper data factory classes."""
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

from apps.scraper.logic.scraped_data.image_scraped_data.image_scraped_data import ImageScrapedData
from apps.scraper.logic.scraped_data.scraped_data import ScrapedData
from apps.scraper.logic.scraped_data.text_scraped_data import TextScrapedData


class Scraper(ABC):
    """Represents base scraper."""

    def __init__(self, website_url: str):
        """
        Initializes properties with params.

        :param website_url: website url to be scraped
        """
        self._website_url = website_url

    def scrape(self):
        """
        Scrapes a website by the given url.

        :return: ScrapedData object
        """
        content = self._get_website_content()
        soup = self._parse_content(content)
        return self._create_scraper_data_instance(soup)

    def _get_website_content(self):
        """
        Sends request to the given website and return its content.

        :return: website content
        """
        return requests.get(self._website_url).content

    @staticmethod
    def _parse_content(content) -> BeautifulSoup:
        """
        Parses website content with BeautifulSoup class.

        :param content: website content
        :return: BeautifulSoup object
        """
        return BeautifulSoup(content, features='html.parser')

    @abstractmethod
    def _create_scraper_data_instance(self, soup: BeautifulSoup) -> ScrapedData:
        """
        Creates scraper data instance.

        :param soup: website content
        :return: ScrapedData instance
        """
        pass


class TextScraper(Scraper):
    """Represents text scraper."""

    def _create_scraper_data_instance(self, soup: BeautifulSoup) -> TextScrapedData:
        """
        Returns TextScrapedData instance.

        :param soup: website content
        :return: TextScrapedData instance
        """
        return TextScrapedData(soup)


class ImageScraper(Scraper):
    """Represents image scraper."""

    def __init__(self, website_url, extension_white_list=None):
        """
        Initializes properties.

        :param website_url: website url to be scraped
        """
        super().__init__(website_url)
        self._extension_white_list = extension_white_list

    def _create_scraper_data_instance(self, soup: BeautifulSoup) -> ImageScrapedData:
        """
        Returns ImageScrapedData instance.

        :param soup: website content
        :return: ImageScrapedData instance
        """
        return ImageScrapedData(soup, self._extension_white_list)
