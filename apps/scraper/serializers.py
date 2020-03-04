"""This module contains scraper app serializers."""
from rest_framework import serializers

from apps.scraper.models import URLModel, ImageScraperModel, TextScraperModel


class TextScraperSerializer(serializers.ModelSerializer):
    """Serializes scraped text."""

    class Meta:
        model = TextScraperModel
        fields = ('id', 'text')


class TextScraperURLSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes urls for text scrapping."""
    text = TextScraperSerializer(source='text_scraper', many=False, read_only=True)

    class Meta:
        model = URLModel
        fields = (
            'id', 'url', 'website_url', 'text', 'request_sent_datetime', 'status', 'request_done_datetime')
        read_only_fields = ('status', 'request_done_datetime')


class ImageScraperSerializer(serializers.ModelSerializer):
    """Serializes scraped images."""

    class Meta:
        model = ImageScraperModel
        fields = ('id', 'image')
        read_only_fields = ('image',)


class ImageScraperURLSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes urls for image scrapping."""
    images = ImageScraperSerializer(source='image_scraper', many=True, read_only=True)

    class Meta:
        model = URLModel
        fields = (
            'id', 'url', 'website_url', 'images', 'request_sent_datetime', 'status', 'request_done_datetime')
        read_only_fields = ('status', 'request_done_datetime')
