from flask import current_app as app, Blueprint
from flask import request, jsonify, abort
import uuid
from datetime import datetime
import pytz
from app import db, models


views_bp = Blueprint('views', __name__)

users = {}
categories = {}
records = {}

@views_bp.route('/')
def index():
    return "Welcome to my Flask App!", 200

@views_bp.route('/healthcheck')
def healthcheck():
    kiev_timezone = pytz.timezone("Europe/Kiev")
    current_time = datetime.now(kiev_timezone).isoformat()
    return f"Server is running! {current_time}", 200

@views_bp.post('/user')
def create_user():
    user_data = request.get_json()
    currency_id = request.args.get("currency_id")  # Передача currency_id через параметр URL

    # Якщо currency_id не передано, шукаємо валюту за замовчуванням (USD)
    if not currency_id:
        default_currency = models.Currency.query.filter_by(code="USD").first()
        if not default_currency:
            abort(500, description="Default currency (USD) is not available in the system.")
        currency_id = default_currency.id

    # Перевірка, чи існує валюта з переданим currency_id
    selected_currency = models.Currency.query.get(currency_id)
    if not selected_currency:
        abort(400, description="Invalid currency_id provided.")

    # Створення нового користувача
    user_id = uuid.uuid4().hex
    new_user = models.User(id=user_id, name=user_data["name"], default_currency_id=currency_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "name": new_user.name,
        "default_currency": {"id": selected_currency.id, "name": selected_currency.name, "code": selected_currency.code}
    }), 201

@views_bp.get('/users')
def get_users():
    users = models.User.query.all()
    response = []

    for user in users:
        # Перевіряємо, чи є валюта
        currency = models.Currency.query.get(user.default_currency_id)

        # Формуємо відповідь
        if currency:
            response.append({
                "id": user.id,
                "name": user.name,
                "default_currency": {
                    "id": currency.id,
                    "name": currency.name,
                    "code": currency.code
                }
            })
        else:
            response.append({
                "id": user.id,
                "name": user.name,
                "default_currency": None  # Валюта відсутня
            })

    return jsonify(response), 200

@views_bp.get('/user/<user_id>')
def get_user(user_id):
    user = models.User.query.get(user_id)
    if not user:
        abort(404, description="User not found.")
    currency = models.Currency.query.get(user.default_currency_id)
    return jsonify({
        "id": user.id,
        "name": user.name,
        "default_currency": {
            "id": currency.id,
            "name": currency.name,
            "code": currency.code
        }
    }), 200

@views_bp.delete('/user/<user_id>')
def delete_user(user_id):
    user = models.User.query.get(user_id)
    if not user:
        abort(404, description="User not found.")
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

@views_bp.put('/user/<user_id>/currency/<currency_id>')
def set_user_currency(user_id, currency_id):
    # Перевіряємо користувача
    user = models.User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    # Перевіряємо валюту
    currency = models.Currency.query.get(currency_id)
    if not currency:
        abort(404, description="Currency not found")

    # Встановлюємо нову валюту
    user.default_currency_id = currency_id
    db.session.commit()

    return jsonify({
        "message": "Currency updated successfully",
        "user_id": user_id,
        "new_currency": {
            "id": currency.id,
            "name": currency.name,
            "code": currency.code
        }
    }), 200

@views_bp.post('/category')
def create_category():
    category_data = request.get_json()
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data}
    categories[category_id] = category
    return jsonify(category), 201

@views_bp.get('/categories')
def get_categories():
    return jsonify(list(categories.values())), 200

@views_bp.get('/category/<category_id>')
def get_category(category_id):
    category = categories.get(category_id)
    if category is None:
        abort(404, description="Category not found")
    return jsonify(category), 200

@views_bp.delete('/category/<category_id>')
def delete_category(category_id):
    category = categories.pop(category_id, None)
    if category is None:
        abort(404, description="Category not found")
    return jsonify({"message": "Category deleted successfully"}), 200


@views_bp.post('/record')
def create_record():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    currency_id = request.args.get("currency_id")  # Новий параметр для вказівки валюти
    data = request.get_json()
    amount = data.get("amount")

    # Перевірка обов'язкових полів
    if not user_id or not category_id or not amount:
        abort(400, description="user_id, category_id, and amount are required")

    # Перевірка існування користувача
    user = models.User.query.get(user_id)
    if not user:
        abort(404, description="User not found.")

    # Перевірка існування категорії
    category = categories.get(category_id)
    if not category:
        abort(404, description="Category not found.")

    # Встановлення валюти: якщо currency_id передано, перевіряємо його; якщо ні, беремо валюту за замовчуванням
    if currency_id:
        currency = models.Currency.query.get(currency_id)
        if not currency:
            abort(400, description="Invalid currency_id provided.")
    else:
        currency = models.Currency.query.get(user.default_currency_id)

    # Створення запису
    record_id = uuid.uuid4().hex
    kiev_timezone = pytz.timezone("Europe/Kiev")
    record = {
        "id": record_id,
        "user_id": user_id,
        "category_id": category_id,
        "currency": {"id": currency.id, "name": currency.name, "code": currency.code},
        "amount": amount,
        "timestamp": datetime.now(kiev_timezone).isoformat()
    }
    records[record_id] = record

    return jsonify(record), 201

@views_bp.get('/record/<record_id>')
def get_record(record_id):
    record = records.get(record_id)
    if not record:
        abort(404, description="Record not found")
    return jsonify(record), 200

@views_bp.delete('/record/<record_id>')
def delete_record(record_id):
    record = records.pop(record_id, None)
    if not record:
        abort(404, description="Record not found")
    return jsonify({"message": "Record deleted successfully"}), 200

@views_bp.get('/record')
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id and not category_id:
        abort(400, description="At least one filter parameter is required (user_id, category_id)")

    filtered_records = [
        record for record in records.values()
        if (not user_id or record["user_id"] == user_id) and (not category_id or record["category_id"] == category_id)
    ]
    return jsonify(filtered_records), 200

@views_bp.post('/currency')
def create_currency():
    data = request.get_json()
    currency = models.Currency(
        id=uuid.uuid4().hex,
        name=data["name"],
        code=data["code"]
    )
    db.session.add(currency)
    db.session.commit()
    return jsonify({"id": currency.id, "name": currency.name, "code": currency.code}), 201

@views_bp.get('/currencies')
def get_currencies():
    currencies = models.Currency.query.all()
    return jsonify([{"id": currency.id, "name": currency.name, "code": currency.code} for currency in currencies]), 200

@views_bp.get('/currency/<currency_id>')
def get_currency(currency_id):
    currency = models.Currency.query.get(currency_id)
    if not currency:
        abort(404, description="Currency not found")
    return jsonify({"id": currency.id, "name": currency.name, "code": currency.code}), 200
