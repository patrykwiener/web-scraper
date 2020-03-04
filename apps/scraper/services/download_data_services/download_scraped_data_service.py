"""
This module contains DownloadScrapedDataService base responsible for creating http response with scraped data.
"""
from apps.scraper.models import URLModel


class DownloadScrapedDataService:

    def __init__(self, url_model: URLModel):
        self._url_model = url_model

    def _create_file_name(self):
        """Returns file name."""
        return '{}_{}_{}'.format(
            self._url_model.id,
            self._url_model.website_url,
            self._url_model.request_done_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
        )

    @staticmethod
    def _remove_redundant_chars(file_name: str) -> str:
        """Removes redundant characters from the file name."""
        return file_name.replace('://', '_').replace('/', '_')

    def _get_file_name(self) -> str:
        """Returns file name containing scraped data."""
        file_name = self._create_file_name()
        cleaned_file_name = self._remove_redundant_chars(file_name)
        return cleaned_file_name
