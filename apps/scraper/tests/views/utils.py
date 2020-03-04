"""This module contains view tests utils."""
import json


def unpack_json(response):
    """Unpacks response content from JSON."""
    return json.loads(response.content)
