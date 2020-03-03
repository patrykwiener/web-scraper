"""This module contains TextScrapedData class representing scraped text from the given website."""
from apps.scraper.logic.scraped_data.scraped_data import ScrapedData


class TextScrapedData(ScrapedData):
    """Represents website scraped text."""

    @property
    def text(self, separator='\n', strip=True):
        """
        Converts website content to text.

        :param separator: strings are concatenated using this separator
        :param strip: if True, strings are stripped before concatenation
        :return: converted website html to text
        """
        return self._soup_page.get_text(separator=separator, strip=strip)
