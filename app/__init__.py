from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # This still points to the login route

# Return JSON for unauthorized access instead of redirecting
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'message': 'Unauthorized - Please log in'}), 401

from app import routes, models

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': user_id})
    if user_data:
        return models.User(**user_data)
    return None