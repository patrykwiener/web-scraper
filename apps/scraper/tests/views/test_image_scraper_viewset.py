import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils import timezone

from apps.scraper.models import URLModel, ImageScraperModel
from apps.scraper.tests.views.utils import unpack_json
from web_scraper.settings import TEST_IMAGES_DIR


class TestImageScraperViewSet(TestCase):
    SAMPLE_URL = 'http://sample.com'
    URL_MODEL_ID = None

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
        cls.URL_MODEL_ID = url_model.id

    def test_post_no_website_url(self):
        response = self.client.post('/image-scraper/', {})
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_website_url(self):
        response = self.client.post('/image-scraper/', {'website_url': 'asd'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(unpack_json(response)['website_url'], ['Enter a valid URL.'])

    def test_post_not_existing_website(self):
        website_url = 'http://asd.asd'
        response = self.client.post('/image-scraper/', {'website_url': website_url}, format='json')
        self.assertEqual(response.status_code, 201)

        unpacked_json = unpack_json(response)
        self.assertEqual(unpacked_json['status'], 'error type: ConnectionError')
        self.assertEqual(unpacked_json['website_url'], website_url)
        self.assertEqual(unpacked_json['images'], [])

        model_id = unpacked_json['id']
        url_model = URLModel.objects.filter(id=model_id)
        self.assertTrue(url_model.exists())
        self.assertEqual(url_model.first().status, 'error type: ConnectionError')

    def test_post_valid_website_url(self):
        website_url = 'https://firstsiteguide.com/what-is-blog/'
        response = self.client.post('/image-scraper/', {'website_url': website_url}, format='json')
        self.assertEqual(response.status_code, 201)

        unpacked_json = unpack_json(response)
        self.assertEqual(unpacked_json['status'], 'done')
        self.assertEqual(unpacked_json['website_url'], website_url)
        self.assertIsNot(unpacked_json['images'], [])

        model_id = unpacked_json['id']
        url_model = URLModel.objects.filter(id=model_id)
        self.assertTrue(url_model.exists())

        url_model = url_model.first()
        self.assertEqual(url_model.status, 'done')
        self.assertTrue(url_model.image_scraper.exists())

    def test_get_all(self):
        response = self.client.get('/image-scraper/')
        self.assertEqual(response.status_code, 200)

        unpacked_json = unpack_json(response)
        self.assertTrue(len(unpacked_json['results']) == 1)

        first_result = unpacked_json['results'][0]
        self.assertEqual(first_result['website_url'], self.SAMPLE_URL)
        self.assertEqual(first_result['status'], URLModel.DONE)
        self.assertIsNot(first_result['images'], [])

        images = first_result['images']
        self.assertEqual(len(images), 2)

    def test_get_specific_image_scraping_instance_not_exists(self):
        response = self.client.get('/image-scraper/200/')
        self.assertEqual(response.status_code, 404)

    def test_get_specific_image_scraping_instance(self):
        response = self.client.get('/image-scraper/{}/'.format(self.URL_MODEL_ID))
        self.assertEqual(response.status_code, 200)

        unpacked_json = unpack_json(response)
        self.assertEqual(unpacked_json['website_url'], self.SAMPLE_URL)
        self.assertEqual(unpacked_json['status'], URLModel.DONE)
        self.assertIsNot(unpacked_json['images'], [])

        images = unpacked_json['images']
        self.assertEqual(len(images), 2)
