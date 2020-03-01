"""This module contains scraper app serializers."""
from rest_framework import serializers

from apps.scraper.models import URLModel


class TextScraperSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes urls for text scrapping."""
    text_scraper = serializers.StringRelatedField(many=False)

    class Meta:
        model = URLModel
        fields = (
            'id', 'url', 'website_url', 'text_scraper', 'request_sent_datetime', 'status', 'request_done_datetime')
        read_only_fields = ('text', 'status', 'request_done_datetime')


class ImageScraperSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes urls for image scrapping."""
    image_scraper = serializers.StringRelatedField(many=True)

    class Meta:
        model = URLModel
        fields = (
            'id', 'url', 'website_url', 'image_scraper', 'request_sent_datetime', 'status', 'request_done_datetime')
        read_only_fields = ('image_scraper', 'status', 'request_done_datetime')
