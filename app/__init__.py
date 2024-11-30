from flask.cli import AppGroup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models
    from app.views import views_bp

    app.register_blueprint(views_bp)

    def add_default_currency():
        with app.app_context():
            if not models.Currency.query.filter_by(code="USD").first():
                usd_currency = models.Currency(
                    id=uuid.uuid4().hex, name="US Dollar", code="USD"
                )
                db.session.add(usd_currency)
                db.session.commit()
                print("Default currency 'USD' added.")

    # Створення команди Flask
    cli = AppGroup("init")
    cli.command("add_default_currency")(add_default_currency)
    app.cli.add_command(cli)

    return app
