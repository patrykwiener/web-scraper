"""This module contains scraper app url definitions."""
from django.urls import path, include
from rest_framework import routers

from apps.scraper.views import TextScraperViewSet, ImageScraperViewSet

router = routers.DefaultRouter()
router.register('text-scraper', TextScraperViewSet)
router.register('image-scraper', ImageScraperViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
