from app import app
from flask import request, jsonify, abort
import uuid


# Словник для зберігання даних про користувачів
users = {}
# Словник для зберігання даних про категорії
categories = {}

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
    category[category_id] = category
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

