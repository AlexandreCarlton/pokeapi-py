
from functools import lru_cache

import requests

@lru_cache(maxsize=None)
def load_json(url: str):
    """Simple function to download and memoize JSON from a given URL"""
    return requests.get(url).json()
