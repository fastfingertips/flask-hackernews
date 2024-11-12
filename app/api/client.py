import requests
import time

from .constants import HN_API_BASE, STORY_TYPES

def get_req(url, timeout=5):
    while True:
        try: return requests.get(url, timeout=timeout)
        except requests.ConnectionError:
            print("No internet connection available.", end='\r')
            time.sleep(1)

def get_hn_item(item_id):
    url = f'{HN_API_BASE}/item/{item_id}.json'
    return get_req(url).json()

def get_stories_by_type(story_type):
    if story_type not in STORY_TYPES:
        raise ValueError(f"Geçersiz story tipi. Geçerli tipler: {list(STORY_TYPES.keys())}")
    url = f'{HN_API_BASE}/{STORY_TYPES[story_type]}.json'
    return get_req(url).json() 