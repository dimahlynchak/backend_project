from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Ініціалізація SQLAlchemy і Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()  # Завантаження змінних середовища
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Підключення SQLAlchemy та Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Імпорт моделей і маршрутів
    with app.app_context():
        from app import models, views

    return app
