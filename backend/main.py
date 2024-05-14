import mysql.connector
import serial
from flask import Flask, jsonify, request
from flask_cors import CORS
from chat import get_response

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

ser = serial.Serial("COM3", 9600)

try:
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="bogda765",
        database="health_data",
    )
    print("Database connection successful")
except Exception as e:
    print(f"Failed to connect to database: {e}")


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
    try:
        ser.write(b"1")
        data = ser.readline().decode().strip()
        hb_data = data.split(":")[1].strip()
        user_email = request.headers.get("Authorization").split(" ")[1]

        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "INSERT INTO health_data (heart_rate, user_email) VALUES (%s, %s)",
            (hb_data, user_email),
        )
        db_connection.commit()
        db_cursor.close()
        print("Data saved successfully")
        return jsonify({"message": "Button pressed, data saved"}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/data")
def get_data():
    user_email = request.headers.get("Authorization").split(" ")[1]
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute(
        "SELECT heart_rate, created_at FROM health_data WHERE user_email = %s ORDER BY id DESC LIMIT 10",
        (user_email,),
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


@app.route("/user", methods=["GET", "PUT"])
def user_profile():
    if request.method == "GET":
        user_email = request.headers.get("Authorization").split(" ")[1]
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute(
            "SELECT name, surname, email, phone_number, address FROM users WHERE email = %s",
            (user_email,),
        )
        user_data = db_cursor.fetchone()
        db_cursor.close()
        if user_data:
            return jsonify({"user": user_data}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == "PUT":
        user_email = request.headers.get("Authorization").split(" ")[1]
        user_data = request.json
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "UPDATE users SET name = %s, surname = %s, phone_number = %s, address = %s WHERE email = %s",
            (user_data["name"], user_data["surname"], user_data["phone_number"], user_data["address"], user_email),
        )
        db_connection.commit()
        db_cursor.close()
        return jsonify({"message": "User data updated successfully"}), 200


if __name__ == "__main__":
    app.run(port=5000)
