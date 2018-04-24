import os
import requests
from lxml.html.clean import Cleaner
import jieba.analyse

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


# https://stackoverflow.com/questions/3073881/clean-up-html-in-python
def sanitize(dirty_html):
    cleaner = Cleaner(page_structure=True,
                  meta=True,
                  embedded=True,
                  links=True,
                  style=True,
                  processing_instructions=True,
                  inline_style=True,
                  scripts=True,
                  javascript=True,
                  comments=True,
                  frames=True,
                  forms=True,
                  annoying_tags=True,
                  remove_unknown_tags=True,
                  safe_attrs_only=True,
                  safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
                  remove_tags=('span', 'font', 'div')
                  )

    return cleaner.clean_html(dirty_html)


def extractContentToDatabase(newsId: int, url: str):
    data = extractContentFromUrl(url)
    with get_session() as session:
        for doc in session.query(Document)\
            .filter(Document.id == newsId):
            doc.mercury_data = data

            docTitle = data['title']
            dirtyContent = data['content']
            cleanedContent = sanitize(dirtyContent)
            doc_words = jieba.analyse.textrank(
                docTitle + ' ' + cleanedContent,
                topK=50,
                withWeight=False,
                allowPOS=('ns', 'n', 'vn', 'v')
            )
