from app.database import get_db_connection


def get_doctors(position=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if position:
        cursor.execute("SELECT * FROM doctors WHERE position LIKE %s", ("%" + position + "%",))
    else:
        cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    return doctors


def get_doctor_by_id(doctor_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()
    cursor.close()
    return doctor
