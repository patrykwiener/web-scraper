"""This module contains Image class representing pulled image from a website."""
from apps.scraper.logic.scraped_data.image_scraped_data.image_url import ImageURL


class Image:
    """Represents pulled image from a website."""

    def __init__(self, image_url: ImageURL, content):
        """
        Initializes object.

        :param image_url: ImageURL object containing pulled image url
        :param content: pulled image content
        """
        self._image_url = image_url
        self._content = content

    @property
    def filename(self):
        """Returns image name with extension."""
        return self._image_url.cleared_after_extension.rsplit(sep='/', maxsplit=1)[1]

    @property
    def content(self):
        """Returns image content."""
        return self._content
