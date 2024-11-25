from app import db

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    default_currency_id = db.Column(db.String, db.ForeignKey('currency.id'))

class Currency(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False, unique=True)
