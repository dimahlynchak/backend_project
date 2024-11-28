import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Ініціалізація SQLAlchemy і Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import views, models
        db.create_all()

        if not models.Currency.query.filter_by(code="USD").first():
            usd_currency = models.Currency(id=uuid.uuid4().hex, name="US Dollar", code="USD")
            db.session.add(usd_currency)
            db.session.commit()

    return app

