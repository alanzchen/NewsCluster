from flask_sqlalchemy import SQLAlchemy
from app import db

class NewsCluster(db.Model):
    __tablename__ = 'cluster' 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True, nullable=False)
    docs = db.Column(db.JSON)
    state = db.Column(db.JSON)

    def __repr__(self):
        return '<Cluster %r>' % self.title
