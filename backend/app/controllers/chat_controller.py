from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import get_db_connection
from app.services.chat_service import add_chat_message, get_user_chat_history
from chatbot.chat import get_response

chat_blueprint = Blueprint('chat', __name__)


@chat_blueprint.route("/history", methods=["GET"])
@jwt_required()
def get_chat_history():
    user_email = get_jwt_identity()
    chat_history = get_user_chat_history(user_email)
    return jsonify(chat_history), 200


@chat_blueprint.route("/message", methods=["POST"])
@jwt_required()
def save_chat_message_endpoint():
    user_email = get_jwt_identity()
    message = request.json.get("message")
    sender = request.json.get("sender")
    response = add_chat_message(user_email, message, sender)
    return jsonify(response), 201


@chat_blueprint.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    text = request.get_json().get("message")
    try:
        with get_db_connection() as connection:
            with connection.cursor() as db_cursor:
                response = get_response(text, db_cursor)

        message = {"answer": response}
        return jsonify(message), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred during prediction"}), 500
