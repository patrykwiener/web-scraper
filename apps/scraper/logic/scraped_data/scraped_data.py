"""This module contains ScrapedData class representing scraped data from the given website."""
from bs4 import BeautifulSoup


class ScrapedData:
    """Represents scraper base class."""

    EXCLUDE_TAGS_LIST = ['script', 'style']

    def __init__(self, soup: BeautifulSoup):
        """
        Initializes properties.

        :param soup: BeautifulSoup object containing website content
        """
        self._soup_page = soup

    def exclude_tags(self, exclude_tags_list=None):
        """
        Excludes given tags from further evaluation.

        :param exclude_tags_list: list of tags to exclude
        """
        if exclude_tags_list is None:
            exclude_tags_list = self.EXCLUDE_TAGS_LIST
        for script in self._soup_page(exclude_tags_list):
            script.decompose()
