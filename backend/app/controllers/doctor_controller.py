from flask import Blueprint, jsonify, request
from app.services.doctor_service import get_doctors, get_doctor_by_id

doctor_blueprint = Blueprint('doctors', __name__)


@doctor_blueprint.route("/", methods=["GET"])
def list_doctors():
    position = request.args.get("position")
    doctors = get_doctors(position)
    return jsonify(doctors), 200


@doctor_blueprint.route("/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    if doctor:
        return jsonify(doctor), 200
    else:
        return jsonify({"error": "Doctor not found"}), 404
