"""This module contains ImageScrapedData class representing scraped images from the given website."""
import requests

from apps.scraper.logic.scraped_data.image_scraped_data.image import Image
from apps.scraper.logic.scraped_data.image_scraped_data.image_url import ImageURL
from apps.scraper.logic.scraped_data.scraped_data import ScrapedData


class ImageScrapedData(ScrapedData):
    """Represents website scraped images."""

    def __init__(self, soup, extension_white_list=None):
        """
        Initializes object properties.

        :param soup: scraped website content
        :param extension_white_list: list of extensions allowed for images
        """
        super().__init__(soup)
        self._extension_white_list = extension_white_list

    def _get_image_url(self, image_tag):
        """
        Gets and validates image source url from the given image tag.

        :param image_tag: website html image tag
        :return: ImageURL object when image source url is valid, None otherwise
        """
        url = image_tag.get('src')
        image_url = ImageURL(url, self._extension_white_list)
        if image_url.is_valid():
            return image_url
        return None

    def _get_image_urls(self):
        """
        Gets all image source urls from the given website.

        :return: list of image source urls
        """
        image_tags = self._soup_page.find_all('img')
        image_urls = []
        for image_tag in image_tags:
            image_url = self._get_image_url(image_tag)
            if image_url:
                image_urls.append(image_url)
        return image_urls

    @staticmethod
    def _pull_image(image_url):
        """
        Pulls an image from a website using the given image url.

        :param image_url: absolute image address
        :return: Image object containing image url address and image content
        """
        content = requests.get(image_url.cleared_after_extension).content
        return Image(image_url, content)

    def pull_images(self):
        """
        Pulls all images from a website.

        :return: list of Image objects representing website images
        """
        image_urls = self._get_image_urls()
        images = []
        for image_url in image_urls:
            image = self._pull_image(image_url)
            images.append(image)
        return images
