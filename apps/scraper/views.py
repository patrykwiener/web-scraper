"""This module contains scraper app view classes."""
import datetime

from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from rest_framework import viewsets, mixins

from apps.scraper.logic.image_scraper.image_scraper import ImageScraper
from apps.scraper.models import URLModel, TextScraperModel, ImageScraperModel
from apps.scraper.serializers import TextScraperURLSerializer, ImageScraperURLSerializer
from apps.scraper.logic.text_scraper import TextScraper


class TextScraperViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """API endpoint for scrapping text."""
    queryset = URLModel.objects.filter(scrapping=URLModel.TEXT)
    serializer_class = TextScraperURLSerializer

    def perform_create(self, serializer):
        serializer.save(scrapping=URLModel.TEXT)
        website_url = serializer.validated_data.get('website_url')
        text_scraper = TextScraper(website_url)
        text_scraper.exclude_tags()
        text = text_scraper.text
        TextScraperModel.objects.create(
            url=serializer.instance,
            text=text,
        )
        serializer.instance.status = URLModel.DONE
        serializer.instance.request_done_datetime = make_aware(datetime.datetime.now())
        serializer.instance.save()


class ImageScraperViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """API endpoint for scrapping images."""
    queryset = URLModel.objects.filter(scrapping=URLModel.IMAGES)
    serializer_class = ImageScraperURLSerializer

    def perform_create(self, serializer):
        serializer.save(scrapping=URLModel.IMAGES)
        website_url = serializer.validated_data.get('website_url')
        image_scraper = ImageScraper(website_url)
        image_scraper.exclude_tags()
        images = image_scraper.pull_images()
        for image in images:
            image_content = ContentFile(image.content)
            image_scraper_model = ImageScraperModel()
            image_scraper_model.url = serializer.instance
            image_scraper_model.image.save(name=image.filename, content=image_content)
            image_scraper_model.save()
        serializer.instance.status = URLModel.DONE
        serializer.instance.request_done_datetime = make_aware(datetime.datetime.now())
        serializer.instance.save()
