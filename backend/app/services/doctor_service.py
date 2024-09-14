from app.repositories.doctor_repository import get_doctors, get_doctor_by_id


def list_doctors(position=None):
    return get_doctors(position)


def get_doctor(doctor_id):
    return get_doctor_by_id(doctor_id)
