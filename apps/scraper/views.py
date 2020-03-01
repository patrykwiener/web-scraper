"""This module contains scraper app view classes."""
from rest_framework import viewsets, mixins

from apps.scraper.models import URLModel
from apps.scraper.serializers import TextScraperSerializer, ImageScraperSerializer


class TextScraperViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """View for scrapping text."""
    queryset = URLModel.objects.filter(scrapping=URLModel.TEXT)
    serializer_class = TextScraperSerializer

    def perform_create(self, serializer):
        return serializer.save(scrapping=URLModel.TEXT)


class ImageScraperViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """View for scrapping images."""
    queryset = URLModel.objects.filter(scrapping=URLModel.IMAGES)
    serializer_class = ImageScraperSerializer

    def perform_create(self, serializer):
        return serializer.save(scrapping=URLModel.IMAGES)
