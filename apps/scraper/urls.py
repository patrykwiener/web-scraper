"""This module contains scraper app url definitions."""
from django.urls import path, include
from rest_framework import routers

from apps.scraper.views import TextScraperViewSet, ImageScraperViewSet, DownloadScrapedDataViewSet

router = routers.DefaultRouter()
router.register('text-scraper', TextScraperViewSet)
router.register('image-scraper', ImageScraperViewSet)
router.register('download-scraped-data', DownloadScrapedDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
