from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.String, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
