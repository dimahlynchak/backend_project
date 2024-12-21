from flask import Blueprint, request, jsonify, abort
import uuid
from datetime import datetime
import pytz

blueprint = Blueprint('main', __name__)

users = {}
categories = {}
records = {}

@blueprint.route('/')
def index():
    return "Welcome to my Flask App!", 200

@blueprint.route('/healthcheck')
def healthcheck():
    kiev_timezone = pytz.timezone("Europe/Kiev")
    current_time = datetime.now(kiev_timezone).isoformat()
    return f"Server is running! {current_time}", 200


@blueprint.post('/user')
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users[user_id] = user
    return jsonify(user), 201

@blueprint.get('/users')
def get_users():
    return jsonify(list(users.values())), 200

@blueprint.get('/user/<user_id>')
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user), 200

@blueprint.delete('/user/<user_id>')
def delete_user(user_id):
    user = users.pop(user_id, None)
    if user is None:
        abort(404, description="User not found")
    return jsonify({"message": "User deleted successfully"}), 200

@blueprint.post('/category')
def create_category():
    category_data = request.get_json()
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data}
    categories[category_id] = category
    return jsonify(category), 201

@blueprint.get('/categories')
def get_categories():
    return jsonify(list(categories.values())), 200

@blueprint.get('/category/<category_id>')
def get_category(category_id):
    category = categories.get(category_id)
    if category is None:
        abort(404, description="Category not found")
    return jsonify(category), 200

@blueprint.delete('/category/<category_id>')
def delete_category(category_id):
    category = categories.pop(category_id, None)
    if category is None:
        abort(404, description="Category not found")
    return jsonify({"message": "Category deleted successfully"}), 200


@blueprint.post('/record')
def create_record():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    data = request.get_json()
    amount = data.get("amount")

    if not user_id or not category_id:
        abort(400, description="user_id and category_id are required")

    if user_id not in users or category_id not in categories:
        abort(400, description="Invalid user_id or category_id")

    record_id = uuid.uuid4().hex
    kiev_timezone = pytz.timezone("Europe/Kiev")
    record = {
        "id": record_id,
        "user_id": user_id,
        "category_id": category_id,
        "amount": amount,
        "timestamp": datetime.now(kiev_timezone).isoformat()
    }
    records[record_id] = record
    return jsonify(record), 201

@blueprint.get('/record/<record_id>')
def get_record(record_id):
    record = records.get(record_id)
    if not record:
        abort(404, description="Record not found")
    return jsonify(record), 200

@blueprint.delete('/record/<record_id>')
def delete_record(record_id):
    record = records.pop(record_id, None)
    if not record:
        abort(404, description="Record not found")
    return jsonify({"message": "Record deleted successfully"}), 200

@blueprint.get('/record')
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