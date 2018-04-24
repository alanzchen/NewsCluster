from sqlalchemy import Column, Integer, Text, JSON
from sqlalchemy import ForeignKey

from models import Base

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    mercury_data = Column(JSON, nullable=True)
    words_data = Column(JSON, nullable=True)
    news_id = Column(Integer, ForeignKey('news.id'))

    def __repr__(self):
        return '<Document %r>' % self.title
