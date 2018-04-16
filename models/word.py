from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy import ForeignKey

from models import Base

class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    frequency = Column(Float, nullable=False)
    news_id = Column(Integer, ForeignKey('news.id'))

    def __repr__(self):
        return '<Word %r>' % self.content

