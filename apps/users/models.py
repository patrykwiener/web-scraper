"""This module contains users app all models definitions."""
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Custom user extending default Django user. This is recommended by Django team."""

    def __str__(self):
        return self.username
