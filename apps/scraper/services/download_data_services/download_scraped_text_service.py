"""
This module contains DownloadScrapedTextService responsible for creating http response with text file containing
scraped text.
"""
import io

from django.http import HttpResponse

from apps.scraper.services.download_data_services.download_scraped_data_service import DownloadScrapedDataService


class DownloadScrapedTextService(DownloadScrapedDataService):
    """Responsible for creating http response with .txt file containing scraped text."""

    def create_download_response(self):
        """
        Creates download http response with .txt file containing scraped text.

        :return: download http response
        """
        text_file_io = self._create_text_file()
        extension = 'txt'
        file_name = self._get_file_name()
        resp = HttpResponse(text_file_io.getvalue(), content_type='text/plain')
        resp['Content-Disposition'] = 'attachment; filename={}.{}'.format(file_name, extension)
        return resp

    def _create_text_file(self):
        """
        Creates .txt file containing scraped text.

        :return: .txt file
        """
        text = self._get_text()
        return io.StringIO(text)

    def _get_text(self):
        """Returns scraped text."""
        return self._url_model.text_scraper.text
