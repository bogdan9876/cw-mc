import mysql.connector
import serial
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ser = serial.Serial('COM3', 9600)

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="bogda765",
    database="health_data"
)


@app.route('/press-button', methods=['POST'])
def press_button():
    ser.write(b'1')
    data = ser.readline().decode().strip()
    hb_data = data.split(":")[1].strip()
    db_cursor = db_connection.cursor()
    db_cursor.execute("INSERT INTO health_data (heart_rate) VALUES (%s)", (hb_data,))
    db_connection.commit()
    db_cursor.close()
    return 'Button pressed, data saved'


@app.route('/api/data')
def get_data():
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT heart_rate FROM health_data ORDER BY id DESC LIMIT 10")
    data = db_cursor.fetchall()
    db_cursor.close()
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000)
