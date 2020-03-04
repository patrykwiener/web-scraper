"""This module contains ImageURL class representing website image absolute url."""
import re


class ImageURL:
    """Represents website image absolute url. The class is responsible for url validation and normalization."""

    EXTENSION_WHITE_LIST = ['jpg', 'png']

    def __init__(self, image_url, extension_white_list=None):
        """
        Initializes ImageURL object.

        :param image_url: website image url
        :param extension_white_list: list of image allowed extensions
        """
        if extension_white_list is None:
            extension_white_list = self.EXTENSION_WHITE_LIST
        self._image_url = image_url
        self._extension_white_list = extension_white_list

    def _is_not_none(self):
        """
        Checks if a url is not none.

        :return: True if a url is not none, False otherwise
        """
        return True if self._image_url else False

    def _is_in_white_list(self):
        """
        Checks if an image has allowed extension.

        :return: True if an image has valid extension, False otherwise
        """
        for ext in self._extension_white_list:
            if re.match(r'^.*\.{}.*$'.format(ext), self._image_url):
                return True
        return False

    def _is_absolute_path(self):
        """
        Checks if a path is absolute.

        :return: match object when path is absolute, None otherwise
        """
        return re.match(r'^http(?:s)?:\/\/.*$', self._image_url)

    def is_valid(self):
        """
        Validates image url.

        :return: True if all tests are passed, False otherwise
        """
        return all([
            self._is_not_none(),
            self._is_absolute_path(),
            self._is_in_white_list(),
        ])

    @property
    def cleared_after_extension(self):
        """
        Clears url after image extension.

        :return: cleared image url
        """
        for ext in self._extension_white_list:
            split_url = self._image_url.rsplit(sep='.{}'.format(ext), maxsplit=1)
            if len(split_url) > 1:
                cleared_url = '{}.{}'.format(split_url[0], ext)
                return cleared_url
        return self._image_url
