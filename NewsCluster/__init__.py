import os
import requests

from models import get_session, Document

MERCURY_TOKEN = os.environ['MERCURY_KEY']
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

def extractContentToDatabase(newsId: int, url: str):
    data = extractContentFromUrl(url)
    with get_session() as session:
        for doc in session.query(Document)\
            .filter(Document.id == newsId):
            doc.mercury_data = data
        session.commit()
