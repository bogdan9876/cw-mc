from app.repositories.health_repository import save_heart_rate, get_recent_heart_rate
from serial_connection import SerialConnection


def record_heart_rate(user_email):
    serial_conn = SerialConnection()
    serial_conn.send_command(b"1")
    data = serial_conn.read_data()
    hb_data = data.split(":")[1].strip()
    save_heart_rate(user_email, hb_data)
    return {"message": "Data saved successfully"}


def retrieve_recent_heart_rate(user_email, limit=10):
    return get_recent_heart_rate(user_email, limit)
