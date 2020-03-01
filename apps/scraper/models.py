"""This module contains scraper app model classes."""
from django.db import models


class URLModel(models.Model):
    """Represents website url to scrapping. Contains present status of the request and operation timestamps."""

    ERROR = 'error'
    PROCESSING = 'processing'
    DONE = 'done'

    STATUS_CHOICES = [
        (ERROR, 'error'),
        (PROCESSING, 'processing'),
        (DONE, 'done'),
    ]

    TEXT = 'text'
    IMAGES = 'images'
    SCRAPPING_CHOICES = [
        (TEXT, 'text'),
        (IMAGES, 'images'),
    ]

    website_url = models.URLField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PROCESSING
    )
    request_sent_datetime = models.DateTimeField(auto_now_add=True)
    request_done_datetime = models.DateTimeField(blank=True, null=True)
    scrapping = models.CharField(
        max_length=10,
        choices=SCRAPPING_CHOICES
    )


class TextScraperModel(models.Model):
    """Represents scraped website text."""
    url = models.OneToOneField(URLModel, on_delete=models.CASCADE, related_name='text_scraper')
    text = models.TextField()


class ImageScraperModel(models.Model):
    """Represents scraped website single image."""
    url = models.ForeignKey(URLModel, on_delete=models.CASCADE, related_name='image_scraper')
    image = models.ImageField(
        upload_to='images/',
        default='pic/folder/None/no-img.jpg'
    )
