from flask_sqlalchemy import SQLAlchemy

import os
from contextlib import contextmanager
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine(os.environ['DATABASE_URL'], echo=True)
SessionMaker = sessionmaker(bind=engine)

Base = declarative_base()

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


class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    news_id = Column(Integer, ForeignKey('news.id'))

    def __repr__(self):
        return '<Document %r>' % self.title


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    frequency = Column(Float, nullable=False)
    news_id = Column(Integer, ForeignKey('news.id'))

    def __repr__(self):
        return '<Word %r>' % self.content


@contextmanager
def get_session():
    session = SessionMaker()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def create_all():
    Base.metadata.create_all(engine)

def clear_all_data():
    print("Clearing all data...")
    with get_session() as session:
        session.query(News).delete()
        session.query(Document).delete()
        session.query(Word).delete()
