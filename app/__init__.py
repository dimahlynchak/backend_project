from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Ініціалізація SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Підключення SQLAlchemy до застосунку
    db.init_app(app)

    # Імпорт маршрутів і моделей
    with app.app_context():
        from app import views, models

    return app
