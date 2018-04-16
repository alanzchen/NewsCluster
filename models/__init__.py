from flask_sqlalchemy import SQLAlchemy

import os
from contextlib import contextmanager
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['DATABASE_URL'], echo=True)
SessionMaker = sessionmaker(bind=engine)

Base = declarative_base()

from models.news import News
from models.document import Document
from models.word import Word


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
        session.query(Word).delete()
        session.query(Document).delete()
        session.query(News).delete()
