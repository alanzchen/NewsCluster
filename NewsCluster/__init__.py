import os
import requests

MERCURY_TOKEN = os.environ['MERCURY_TOKEN']
MERCURY_URL = 'https://mercury.postlight.com/parser?url='

def extractContentFromUrl(url: str):
    """
    - title
    - content
    - date_published
    - lead_image_url
    - dek
    - url
    - domain
    - excerpt
    - word_count
    - direction
    - total_pages
    - rendered_pages
    - next_page_url
    """

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': MERCURY_TOKEN,
    }
    r = requests.get(MERCURY_URL + url, headers=headers)
    return r.json()

def extractContentToDataBase(newsId: int, url: str):
    data = extractContentFromUrl(url)
    pass
