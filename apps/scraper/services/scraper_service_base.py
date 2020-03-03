"""
This module contains ScraperServiceBase abstract class providing connection between models and classes providing
scraping functionality.
"""
import datetime
from abc import ABC, abstractmethod

from django.utils.timezone import make_aware

from apps.scraper.logic.scraper import Scraper
from apps.scraper.logic.scraped_data.scraped_data import ScrapedData
from apps.scraper.models import URLModel


class ScraperServiceBase(ABC):
    """An abstract service class allowing scraping from the given website by combining models and scraping classes."""

    def __init__(self, url_model: URLModel, scraper: Scraper):
        """
        Initializes object with the given params.

        :param url_model: website to be scraped URLModel object
        :param scraper: Scraper object
        """
        self._url_model = url_model
        self._scraper = scraper

    def _set_url_model_status(self, status: str) -> None:
        """
        Sets url model with the given status.

        :param status: scraping final status
        """
        self._url_model.status = status

    def _set_request_done_timestamp(self) -> None:
        """Sets request completion datetime with the current datetime."""
        self._url_model.request_done_datetime = make_aware(datetime.datetime.now())

    @abstractmethod
    def _unpack_scraped_data(self, scraped_data: ScrapedData):
        """
        Abstract method returning unpacked scraped data.

        :param scraped_data: ScrapedData object
        """
        pass

    @abstractmethod
    def _create_scraped_data_model(self, unpacked_data):
        """
        Abstract method storing scraped data into database.

        :param unpacked_data: unpacked scraped data
        """
        pass

    def _update_url_model(self, status: str) -> None:
        """
        Updates url model with data gathered after request evaluation.

        :param status: scraping final status
        :return:
        """
        self._set_url_model_status(status)
        self._set_request_done_timestamp()
        self._url_model.save()

    def perform(self) -> None:
        """Executes scraper service by performing scraping process and storing returned data."""
        try:
            scraped_data = self._scraper.scrape()
        except Exception as ex:
            msg = 'error type: {}'.format(ex.__class__.__name__)
            self._update_url_model(msg)
        else:
            scraped_data.exclude_tags()
            unpacked_data = self._unpack_scraped_data(scraped_data)
            self._create_scraped_data_model(unpacked_data)
            self._update_url_model(URLModel.DONE)
