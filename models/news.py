from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from models import Base

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=True)
    docs = relationship('Document', backref='news',
                                lazy='dynamic')
    words = relationship('Word', backref='news',
                                lazy='dynamic')

    def __repr__(self):
        return '<News %r>' % self.title

