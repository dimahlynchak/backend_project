from app import app
from flask import request, jsonify, abort
import uuid
from datetime import datetime


users = {}
categories = {}
records = {}

@app.route('/')
def index():
    return "Welcome to my Flask App!", 200

@app.route('/healthcheck')
def healthcheck():
    return "Server is running!", 200

@app.post('/user')
def create_user():
    user_data = request.get_json()
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data}
    users[user_id] = user
    return jsonify(user), 201

@app.get('/users')
def get_users():
    return jsonify(list(users.values())), 200

@app.get('/user/<user_id>')
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user), 200

@app.delete('/user/<user_id>')
def delete_user(user_id):
    user = users.pop(user_id, None)
    if user is None:
        abort(404, description="User not found")
    return jsonify({"message": "User deleted successfully"}), 200

@app.post('/category')
def create_category():
    category_data = request.get_json()
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data}
    categories[category_id] = category
    return jsonify(category), 201

@app.get('/category/category_id>')
def get_category(category_id):
    category = categories.get(category_id)
    if category is None:
        abort(404, description="Category not found")
    return jsonify(category), 200

@app.delete('/category/<category_id>')
def delete_category(category_id):
    category = categories.pop(category_id, None)
    if category is None:
        abort(404, description="Category not found")
    return jsonify({"message": "Category deleted successfully"}), 200

@app.post('/record')
def create_record():
    data = request.get_json()
    user_id = data.get("user_id")
    category_id = data.get("category_id")
    amount = data.get("amount")

    if user_id not in users or category_id not in categories:
        abort(400, description="Invalid user_id or category_id")

    record_id = uuid.uuid4().hex
    record = {
        "id": record_id,
        "user_id": user_id,
        "category_id": category_id,
        "amount": amount,
        "timestamp": datetime.utcnow().isoformat()
    }
    records[record_id] = record
    return jsonify(record), 201

@app.get('/record/<record_id>')
def get_record(record_id):
    record = records.get(record_id)
    if not record:
        abort(404, description="Record not found")
    return jsonify(record), 200

@app.delete('/record/<record_id>')
def delete_record(record_id):
    record = records.pop(record_id, None)
    if not record:
        abort(404, description="Record not found")
    return jsonify({"message": "Record deleted successfully"}), 200

@app.get('/record')
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
