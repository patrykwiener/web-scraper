"""This module contains scraper app view classes."""
from django.http import Http404
from rest_framework import viewsets, mixins

from apps.scraper.models import URLModel
from apps.scraper.serializers import TextScraperURLSerializer, ImageScraperURLSerializer
from apps.scraper.services.download_data_services.download_scraped_images_service import DownloadScrapedImagesService
from apps.scraper.services.download_data_services.download_scraped_text_service import DownloadScrapedTextService
from apps.scraper.services.scraper_services.image_scraper_service import ImageScraperService
from apps.scraper.services.scraper_services.text_scraper_service import TextScraperService


class TextScraperViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """API endpoint for scrapping text."""
    queryset = URLModel.objects.filter(scrapping=URLModel.TEXT)
    serializer_class = TextScraperURLSerializer

    def perform_create(self, serializer):
        serializer.save(scrapping=URLModel.TEXT)
        text_scraper_service = TextScraperService(serializer.instance)
        text_scraper_service.perform()


class ImageScraperViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """API endpoint for scrapping images."""
    queryset = URLModel.objects.filter(scrapping=URLModel.IMAGES)
    serializer_class = ImageScraperURLSerializer

    def perform_create(self, serializer):
        serializer.save(scrapping=URLModel.IMAGES)
        image_scraper_service = ImageScraperService(serializer.instance)
        image_scraper_service.perform()


class DownloadScrapedDataViewSet(mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """API endpoint for downloading scraped data based on scraped website id."""
    queryset = URLModel.objects.all()

    def get_object(self):
        """
        Returns URLModel object when its status is set to done.

        :return: URLModel object
        """
        obj = super().get_object()
        if obj.status != URLModel.DONE:
            raise Http404
        return obj

    def retrieve(self, request, *args, **kwargs):
        """
        Returns http download response of scraped data from the given website by id. Depending on record association
        returns zipped images or .txt file with website text.
        """
        url_model = self.get_object()  # type: URLModel

        if url_model.image_scraper.exists():
            resp = DownloadScrapedImagesService(url_model).create_download_response()
        elif url_model.text_scraper:
            resp = DownloadScrapedTextService(url_model).create_download_response()
        else:
            raise NotImplementedError
        return resp
