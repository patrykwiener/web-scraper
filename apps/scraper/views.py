"""This module contains scraper app view classes."""
from rest_framework import viewsets, mixins

from apps.scraper.models import URLModel
from apps.scraper.serializers import TextScraperURLSerializer, ImageScraperURLSerializer
from apps.scraper.services.image_scraper_service import ImageScraperService
from apps.scraper.services.text_scraper_service import TextScraperService


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
