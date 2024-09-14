from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

from app.controllers.user_controller import user_blueprint
from app.controllers.health_controller import health_blueprint
from app.controllers.chat_controller import chat_blueprint
from app.controllers.doctor_controller import doctor_blueprint

from app.database import get_db_connection


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(health_blueprint, url_prefix='/health')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    app.register_blueprint(doctor_blueprint, url_prefix='/doctors')

    app.db_connection = get_db_connection()

    return app
