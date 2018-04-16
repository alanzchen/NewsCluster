from flask_sqlalchemy import SQLAlchemy
from app import db

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
    docs = db.relationship('Document', backref='news',
                                lazy='dynamic')
    words = db.relationship('Word', backref='news',
                                lazy='dynamic')

    def __repr__(self):
        return '<News %r>' % self.title


class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __repr__(self):
        return '<Document %r>' % self.title


class Word(db.Model):
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.Float, nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))

    def __repr__(self):
        return '<Word %r>' % self.content
