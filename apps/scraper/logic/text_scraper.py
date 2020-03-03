"""This module contains TextScraper class responsible for fetching text from the given website."""
from apps.scraper.logic.scraper_base import ScraperBase


class TextScraper(ScraperBase):
    """Represents website text scraper."""

    @property
    def text(self, separator='\n', strip=True):
        """
        Converts website html to text.

        :param separator: strings are concatenated using this separator
        :param strip: if True, strings are stripped before concatenation
        :return: converted website html to text
        """
        return self._soup_page.get_text(separator=separator, strip=strip)
