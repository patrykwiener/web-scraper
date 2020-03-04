"""
This module contains ImageScraperService class providing connection between models and classes providing text
scraping functionality.
"""
from apps.scraper.logic.scraped_data.text_scraped_data import TextScrapedData
from apps.scraper.logic.scraper import TextScraper
from apps.scraper.models import TextScraperModel, URLModel
from apps.scraper.services.scraper_services.scraper_service_base import ScraperServiceBase


class TextScraperService(ScraperServiceBase):
    """A service class allowing scraping text from the given website by combining models and scraping classes."""

    def __init__(self, url_model: URLModel):
        """
        Invokes super class constructor by injecting TextScraper class.

        :param url_model: website to be scraped URLModel object
        """
        super().__init__(
            url_model=url_model,
            scraper=TextScraper(url_model.website_url)
        )

    def _unpack_scraped_data(self, scraped_data: TextScrapedData) -> str:
        """
        Returns scraped text.

        :param scraped_data: TextScrapedData object
        :return: scraped text
        """
        return scraped_data.text

    def _create_scraped_data_model(self, unpacked_data: str) -> None:
        """
        Stores scraped text into database.

        :param unpacked_data: scraped text
        """
        TextScraperModel.objects.create(
            url=self._url_model,
            text=unpacked_data,
        )
