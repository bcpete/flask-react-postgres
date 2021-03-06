from app import db
from sqlalchemy.dialects.postgresql import JSON

class BlogPost(db.Model):
    __tablename__ = 'posts'

    id    = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    body  = db.Column(db.String())

    def __init__(self, title, body):
        self.title = title
        self.body = body