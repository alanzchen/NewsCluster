from sqlalchemy import Column, Integer, Text
from sqlalchemy import ForeignKey

from models import Base

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    news_id = Column(Integer, ForeignKey('news.id'))

    def __repr__(self):
        return '<Document %r>' % self.title


