"""
This module contains DownloadScrapedImagesService responsible for creating http response with zipped scraped images.
"""
from io import BytesIO
from os.path import basename
from zipfile import ZipFile

from django.http import HttpResponse

from apps.scraper.models import ImageScraperModel
from apps.scraper.services.download_data_services.download_scraped_data_service import DownloadScrapedDataService


class DownloadScrapedImagesService(DownloadScrapedDataService):
    """Responsible for creating http response with zipped scraped images."""

    def create_download_response(self):
        """
        Creates download http response with zipped scraped images.

        :return: download http response
        """
        zip_file_io = self._create_zip_file()
        content_type = 'application/x-zip-compressed'
        extension = 'zip'
        file_name = self._get_file_name()
        resp = HttpResponse(zip_file_io.getvalue(), content_type=content_type)
        resp['Content-Disposition'] = 'attachment; filename={}.{}'.format(file_name, extension)
        return resp

    def _create_zip_file(self) -> BytesIO:
        """
        Creates io zip file with scraped images.

        :return: zipped scraped images io file
        """
        zip_file_io = BytesIO()
        with ZipFile(zip_file_io, 'w') as zip_file:
            for image_scraper_model in self._url_model.image_scraper.all():
                image_absolute_path = self._get_image_absolute_path(image_scraper_model)
                zip_file_image_path = self._get_zip_file_image_path(image_absolute_path)
                zip_file.write(image_absolute_path, zip_file_image_path)
            zip_file.close()
        return zip_file_io

    def _get_zip_file_image_path(self, image_absolute_path: str) -> str:
        """
        Creates image path in a zip file.

        :param image_absolute_path: image absolute path
        :return: image path in a zip file
        """
        folder_name = self._get_file_name()
        image_name = basename(image_absolute_path)
        return '{}/{}'.format(folder_name, image_name)

    @staticmethod
    def _get_image_absolute_path(image_scraper_model: ImageScraperModel) -> str:
        """
        Returns image absolute path.

        :param image_scraper_model: ImageScraperModel object
        :return: image absolute path
        """
        return image_scraper_model.image.path
