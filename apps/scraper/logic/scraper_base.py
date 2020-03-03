"""This module contains ScraperBase class responsible for core scraping actions."""
import requests
from bs4 import BeautifulSoup


class ScraperBase:
    """Represents scraper base class."""

    EXCLUDE_TAGS_LIST = ['script', 'style']

    def __init__(self, website_url):
        """
        Sends request to the given website. Initializes BeautifulSoup object responsible for most of scraping
        operations.

        :param website_url: website url to be scraped
        """
        page = requests.get(website_url).content
        self._soup_page = BeautifulSoup(page, features='html.parser')

    def exclude_tags(self, exclude_tags_list=None):
        """
        Excludes given tags from further evaluation.

        :param exclude_tags_list: list of tags to exclude
        """
        if exclude_tags_list is None:
            exclude_tags_list = self.EXCLUDE_TAGS_LIST
        self._soup_page = self._soup_page.body
        for script in self._soup_page(exclude_tags_list):
            script.decompose()
