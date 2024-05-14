import mysql.connector
import serial
from flask import Flask, jsonify, request
from flask_cors import CORS
from chat import get_response

app = Flask(__name__)
CORS(app)

ser = serial.Serial("COM3", 9600)

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="bogda765",
    database="health_data",
)


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = db_cursor.fetchone()
    db_cursor.close()

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    db_cursor = db_connection.cursor()
    db_cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    db_connection.commit()
    db_cursor.close()

    return jsonify({"message": "Registration successful"}), 201


@app.route("/press-button", methods=["POST"])
def press_button():
    ser.write(b"1")
    data = ser.readline().decode().strip()
    hb_data = data.split(":")[1].strip()
    user_id = request.json.get("user_id")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT INTO health_data (heart_rate, user_id) VALUES (%s, %s)",
        (hb_data, user_id),
    )
    db_connection.commit()
    db_cursor.close()
    return "Button pressed, data saved"


@app.route("/api/data")
def get_data():
    user_id = request.headers.get("Authorization").split(" ")[1]
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute(
        "SELECT heart_rate, created_at FROM health_data WHERE user_id = %s ORDER BY id DESC LIMIT 10",
        (user_id,),
    )
    data = db_cursor.fetchall()
    db_cursor.close()
    return jsonify(data)


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(port=5000)
