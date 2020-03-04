from django.test import TestCase
from django.utils import timezone

from apps.scraper.models import URLModel, TextScraperModel
from apps.scraper.tests.views.utils import unpack_json


class TestTextScraperViewSet(TestCase):
    SAMPLE_URL = 'http://sample.com'
    SAMPLE_TEXT = 'Sample Text'
    URL_MODEL_ID = None

    @classmethod
    def setUpTestData(cls):
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
        cls.URL_MODEL_ID = url_model_text.id

    def test_post_no_website_url(self):
        response = self.client.post('/text-scraper/', {})
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_website_url(self):
        response = self.client.post('/text-scraper/', {'website_url': 'asd'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(unpack_json(response)['website_url'], ['Enter a valid URL.'])

    def test_post_not_existing_website(self):
        website_url = 'http://asd.asd'
        response = self.client.post('/text-scraper/', {'website_url': website_url}, format='json')
        self.assertEqual(response.status_code, 201)

        unpacked_json = unpack_json(response)
        self.assertEqual(unpacked_json['status'], 'error type: ConnectionError')
        self.assertEqual(unpacked_json['website_url'], website_url)
        self.assertEqual(unpacked_json['text'], None)

        model_id = unpacked_json['id']
        url_model = URLModel.objects.filter(id=model_id)
        self.assertTrue(url_model.exists())
        self.assertEqual(url_model.first().status, 'error type: ConnectionError')

    def test_post_valid_website_url(self):
        website_url = 'https://stackoverflow.com/'
        response = self.client.post('/text-scraper/', {'website_url': website_url}, format='json')
        self.assertEqual(response.status_code, 201)

        unpacked_json = unpack_json(response)
        self.assertEqual(unpacked_json['status'], 'done')
        self.assertEqual(unpacked_json['website_url'], website_url)
        self.assertIsNotNone(unpacked_json['text'])

        model_id = unpacked_json['id']
        url_model = URLModel.objects.filter(id=model_id)
        self.assertTrue(url_model.exists())

        url_model = url_model.first()
        self.assertIn('Stack Overflow', url_model.text_scraper.text)
        self.assertEqual(url_model.status, 'done')
        self.assertFalse(url_model.image_scraper.exists())

    def test_get_all(self):
        response = self.client.get('/text-scraper/')
        self.assertEqual(response.status_code, 200)

        unpacked_json = unpack_json(response)
        self.assertTrue(len(unpacked_json['results']) == 1)

        first_result = unpacked_json['results'][0]
        self.assertEqual(first_result['website_url'], self.SAMPLE_URL)
        self.assertEqual(first_result['status'], URLModel.DONE)
        self.assertIsNotNone(first_result['text'])

        text = first_result['text']
        self.assertEqual(text['text'], self.SAMPLE_TEXT)

    def test_get_specific_text_instance_not_exists(self):
        response = self.client.get('/text-scraper/200/')
        self.assertEqual(response.status_code, 404)

    def test_get_specific_text_instance(self):
        response = self.client.get('/text-scraper/{}/'.format(self.URL_MODEL_ID))
        self.assertEqual(response.status_code, 200)

        unpacked_json = unpack_json(response)
        self.assertEqual(unpacked_json['website_url'], self.SAMPLE_URL)
        self.assertEqual(unpacked_json['status'], URLModel.DONE)
        self.assertIsNotNone(unpacked_json['text'])

        text = unpacked_json['text']
        self.assertEqual(text['text'], self.SAMPLE_TEXT)
