from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Ініціалізація розширень
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Завантаження конфігурації
    app.config.from_object('app.config.Config')

    # Ініціалізація розширень
    db.init_app(app)
    migrate.init_app(app, db)

    # Імпорт моделей
    with app.app_context():
        from app import models

    # Реєстрація Blueprint
    from app.views import bp as views_bp
    app.register_blueprint(views_bp)

    return app