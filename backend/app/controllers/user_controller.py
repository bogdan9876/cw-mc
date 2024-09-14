from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.services.user_service import get_user, register_user, update_profile

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = get_user(email)

    if user and user['password'] == password:
        access_token = create_access_token(identity=email)
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@user_blueprint.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    response = register_user(username, email, password)
    return jsonify(response), 201


@user_blueprint.route("/user", methods=["GET"])
@jwt_required()
def get_user_info():
    user_email = get_jwt_identity()
    user = get_user(user_email)
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_blueprint.route("/user", methods=["PUT"])
@jwt_required()
def update_user_info():
    user_email = get_jwt_identity()
    name = request.json.get("name")
    surname = request.json.get("surname")
    phone_number = request.json.get("phone_number")
    address = request.json.get("address")

    update_profile(user_email, name, surname, phone_number, address)
    return jsonify({"message": "User data updated successfully"}), 200
