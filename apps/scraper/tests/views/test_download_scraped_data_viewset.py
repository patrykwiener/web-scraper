import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils import timezone

from apps.scraper.models import ImageScraperModel, URLModel, TextScraperModel
from web_scraper.settings import TEST_IMAGES_DIR


class TestDownloadScrapedDataViewSet(TestCase):
    SAMPLE_URL = 'http://sample.com'
    SAMPLE_TEXT = 'Sample Text'

    @classmethod
    def create_image_scraper_model(cls, image_path, url_model):
        pil_image = Image.open(image_path)
        bytes_io = BytesIO()
        pil_image.save(bytes_io, format='JPEG')
        file = ContentFile(bytes_io.getvalue())
        image1 = ImageScraperModel()
        image1.url = url_model
        image1.image.save('test1.jpg', file)
        image1.save()

    @classmethod
    def setUpTestData(cls):
        url_model = URLModel.objects.create(
            website_url=cls.SAMPLE_URL,
            status=URLModel.DONE,
            request_done_datetime=timezone.now(),
            scrapping=URLModel.IMAGES
        )
        image_path = os.path.join(TEST_IMAGES_DIR, 'test1.jpg')
        cls.create_image_scraper_model(image_path, url_model)
        image_path = os.path.join(TEST_IMAGES_DIR, 'test2.jpg')
        cls.create_image_scraper_model(image_path, url_model)

        url_model_text = URLModel.objects.create(
            website_url=cls.SAMPLE_URL,
            status=URLModel.DONE,
            request_done_datetime=timezone.now(),
            scrapping=URLModel.TEXT
        )
        TextScraperModel.objects.create(
            url=url_model_text,
            text='Sample Text'
        )

    def test_get_image_scraped_data(self):
        response = self.client.get('/download-scraped-data/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._content_type_for_repr, ', "application/x-zip-compressed"')

    def test_get_text_scraped_data(self):
        response = self.client.get('/download-scraped-data/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response._content_type_for_repr, ', "text/plain"')
