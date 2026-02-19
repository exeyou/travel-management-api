import requests
from django.core.cache import cache

ART_API_BASE = "https://api.artic.edu/api/v1/artworks"


def get_artwork_by_id(external_id: int):

    cache_key = f"artwork_{external_id}"
    cached = cache.get(cache_key)

    if cached:
        return cached

    response = requests.get(f"{ART_API_BASE}/{external_id}")

    if response.status_code != 200:
        return None

    data = response.json().get("data")

    if not data:
        return None

    cache.set(cache_key, data, timeout=3600)

    return data
