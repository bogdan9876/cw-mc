from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.health_service import record_heart_rate, retrieve_recent_heart_rate

health_blueprint = Blueprint('health', __name__)


@health_blueprint.route("/press-button", methods=["POST"])
@jwt_required()
def press_button():
    user_email = get_jwt_identity()
    response = record_heart_rate(user_email)
    return jsonify(response), 200


@health_blueprint.route("/data", methods=["GET"])
@jwt_required()
def get_data():
    user_email = get_jwt_identity()
    data = retrieve_recent_heart_rate(user_email)
    return jsonify(data), 200
