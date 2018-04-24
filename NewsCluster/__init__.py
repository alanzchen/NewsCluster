import os
import requests
from lxml.html.clean import Cleaner
import jieba.analyse

from models import get_session, Document, News

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


def getWordsData(oldData, words):
    data = oldData
    for word in words:
        if word in data:
            data[word] += 1
        else:
            data[word] = 1
    return data


def extractContentToDatabase(id: int, url: str, newsId: int):
    data = extractContentFromUrl(url)
    with get_session() as session:
        for doc in session.query(Document)\
            .filter(Document.id == id):
            doc.mercury_data = data

            docTitle = data['title']
            dirtyContent = data['content']
            cleanedContent = sanitize(dirtyContent)
            docWords = jieba.analyse.textrank(
                docTitle + ' ' + cleanedContent,
                topK=50,
                withWeight=False,
                allowPOS=('ns', 'n', 'vn', 'v')
            )
            oldData = doc.words_data
            if oldData is None:
                oldData = {}
            doc.words_data = getWordsData(oldData, docWords)
    with get_session() as session:
        for news in session.query(News)\
            .filter(News.id == newsId):

            data = news.words_data
            if data is None:
                data = {}

            for docOfNews in session.Document\
                .filter(Document.news_id == newsId):

                docWordsData = docOfNews.words_data
                if docWordsData is not None:
                    for name, count in docWordsData.items():
                        if name in data:
                            data[name] += count
                        else:
                            data[name] = count
            news.words_data = data
