from app import app, mongo
from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User

@app.route('/')
def home():
    return 'Welcome to Asksphere!'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if mongo.db.users.find_one({'username': data['username']}):
        return jsonify({'message': 'User already exists'}), 400
    
    user_data = {'username': data['username'], 'password': data['password']}  # In production, hash the password!
    result = mongo.db.users.insert_one(user_data)
    user = User(str(result.inserted_id), data['username'], data['password'])
    return jsonify({'message': 'User registered successfully', 'id': str(result.inserted_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = mongo.db.users.find_one({'username': data['username']})
    if user_data and user_data['password'] == data['password']:  # In production, use proper password hashing
        user = User(str(user_data['_id']), user_data['username'], user_data['password'])
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': 'This is a protected route', 'user': current_user.username})