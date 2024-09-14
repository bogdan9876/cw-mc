import mysql.connector
from flask import current_app


def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="bogda765",
        database="health_data"
    )
