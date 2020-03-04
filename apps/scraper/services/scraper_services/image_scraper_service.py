"""
This module contains ImageScraperService class providing connection between models and classes providing image
scraping functionality.
"""
from typing import List

from django.core.files.base import ContentFile

from apps.scraper.logic.scraped_data.image_scraped_data.image import Image
from apps.scraper.logic.scraped_data.image_scraped_data.image_scraped_data import ImageScrapedData
from apps.scraper.logic.scraper import ImageScraper
from apps.scraper.models import ImageScraperModel, URLModel
from apps.scraper.services.scraper_services.scraper_service_base import ScraperServiceBase


class ImageScraperService(ScraperServiceBase):
    """A service class allowing scraping images from the given website by combining models and scraping classes."""

    def __init__(self, url_model: URLModel, extension_white_list=None):
        """
        Invokes super class constructor by injecting ImageScraper class.

        :param url_model: website to be scraped URLModel object
        """
        super().__init__(
            url_model=url_model,
            scraper=ImageScraper(url_model.website_url, extension_white_list)
        )

    def _unpack_scraped_data(self, scraped_data: ImageScrapedData) -> List[Image]:
        """
        Returns list of scraped images.

        :param scraped_data: ImageScrapedData object
        :return: list of scraped images
        """
        return scraped_data.pull_images()

    def _create_scraped_data_model(self, unpacked_data: List[Image]) -> None:
        """
        Stores scraped images into database.

        :param unpacked_data: list of scraped images
        """
        for image in unpacked_data:
            image_scraper_model = ImageScraperModel()
            image_scraper_model.url = self._url_model

            image_content = ContentFile(image.content)
            image_scraper_model.image.save(name=image.filename, content=image_content)

            image_scraper_model.save()
