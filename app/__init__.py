from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": "http://localhost:4200",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

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
    return jsonify({
        'message': 'User registered successfully',
        'user': {'id': str(result.inserted_id), 'username': data['username']}
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = mongo.db.users.find_one({'username': data['username']})
    if user_data and bcrypt.check_password_hash(user_data['password'], data['password']):
        return jsonify({
            'message': 'Logged in successfully',
            'user': {'id': str(user_data['_id']), 'username': user_data['username']}
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)