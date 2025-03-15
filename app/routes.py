from app import app, mongo, bcrypt
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
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_data = {'username': data['username'], 'password': hashed_password}
    result = mongo.db.users.insert_one(user_data)
    user = User(str(result.inserted_id), data['username'], hashed_password)
    return jsonify({'message': 'User registered successfully', 'id': str(result.inserted_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = mongo.db.users.find_one({'username': data['username']})
    if user_data and bcrypt.check_password_hash(user_data['password'], data['password']):
        user = User(str(user_data['_id']), user_data['username'], user_data['password'])
        login_user(user)
        # Return user data along with success message
        return jsonify({
            'message': 'Logged in successfully',
            'user': {
                'id': str(user_data['_id']),
                'username': user_data['username']
            }
        }), 200
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

@app.route('/api/users/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({'username': current_user.username, 'id': current_user.get_id()})