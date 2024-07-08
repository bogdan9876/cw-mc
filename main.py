import base64
from datetime import timedelta
import mysql.connector
# import serial
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
# from chat import get_response

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# ser = serial.Serial("COM3", 9600)

try:
    db_connection = mysql.connector.connect(
        host="fojvtycq53b2f2kx.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
        port="3306",
        user="oc0cdpy4ylb0du8t",
        password="konzkdqu9y2gert1",
        database="yh4u9zzndt9ujkg8",
    )
    print("Database connection successful")
except Exception as e:
    print(f"Failed to connect to database: {e}")


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s", (email, password)
    )
    user = db_cursor.fetchone()
    db_cursor.close()
    if user:
        access_token = create_access_token(identity=email)
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, password),
    )
    db_connection.commit()
    db_cursor.close()
    return jsonify({"message": "Registration successful"}), 201


# @app.route("/press-button", methods=["POST"])
# @jwt_required()
# def press_button():
#     ser.write(b"1")
#     data = ser.readline().decode().strip()
#     hb_data = data.split(":")[1].strip()
#     user_email = get_jwt_identity()
#
#     db_cursor = db_connection.cursor()
#     db_cursor.execute(
#         "INSERT INTO health_data (heart_rate, user_email) VALUES (%s, %s)",
#         (hb_data, user_email),
#     )
#     db_connection.commit()
#     db_cursor.close()
#     print("Data saved successfully")
#     return jsonify({"message": "Button pressed, data saved"}), 200


@app.route("/api/data")
@jwt_required()
def get_data():
    user_email = get_jwt_identity()
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute(
        "SELECT heart_rate, created_at FROM health_data WHERE user_email = %s ORDER BY id DESC LIMIT 10",
        (user_email,),
    )
    data = db_cursor.fetchall()
    db_cursor.close()
    return jsonify(data)


# @app.post("/predict")
# @jwt_required()
# def predict():
#     text = request.get_json().get("message")
#     db_cursor = db_connection.cursor()
#     response = get_response(text, db_cursor)
#     message = {"answer": response}
#     return jsonify(message)


@app.route("/user", methods=["GET", "PUT"])
@jwt_required()
def user_profile():
    user_email = get_jwt_identity()
    if request.method == "GET":
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute(
            "SELECT name, surname, email, phone_number, address, profile_picture FROM users WHERE email = %s",
            (user_email,),
        )
        user_data = db_cursor.fetchone()
        db_cursor.close()
        if user_data:
            if user_data["profile_picture"]:
                user_data["profile_picture"] = base64.b64encode(user_data["profile_picture"]).decode('utf-8')
            return jsonify({"user": user_data}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == "PUT":
        user_data = request.json
        profile_picture = user_data.get("profile_picture")
        db_cursor = db_connection.cursor()
        if profile_picture:
            profile_picture = base64.b64decode(profile_picture)
            db_cursor.execute(
                "UPDATE users SET name = %s, surname = %s, phone_number = %s, address = %s, profile_picture = %s WHERE email = %s",
                (
                    user_data["name"],
                    user_data["surname"],
                    user_data["phone_number"],
                    user_data["address"],
                    profile_picture,
                    user_email,
                ),
            )
        else:
            db_cursor.execute(
                "UPDATE users SET name = %s, surname = %s, phone_number = %s, address = %s WHERE email = %s",
                (
                    user_data["name"],
                    user_data["surname"],
                    user_data["phone_number"],
                    user_data["address"],
                    user_email,
                ),
            )
        db_connection.commit()
        db_cursor.close()
        return jsonify({"message": "User data updated successfully"}), 200


@app.route("/doctors", methods=["GET"])
def get_doctors():
    position = request.args.get("position")
    db_cursor = db_connection.cursor(dictionary=True)
    if position:
        db_cursor.execute(
            "SELECT * FROM doctors WHERE position LIKE %s", ("%" + position + "%",)
        )
    else:
        db_cursor.execute("SELECT * FROM doctors")
    doctors = db_cursor.fetchall()
    db_cursor.close()
    return jsonify(doctors), 200


@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = db_cursor.fetchone()
    db_cursor.close()
    if (doctor):
        return jsonify(doctor), 200
    else:
        return jsonify({"error": "Doctor not found"}), 404


@app.route('/chat/history/<int:chat_id>', methods=['OPTIONS', 'GET'])
@jwt_required()
def get_chat_history(chat_id):
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', 'https://pulse-tracker.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        return response
    elif request.method == 'GET':
        user_email = get_jwt_identity()
        db_cursor = db_connection.cursor(dictionary=True)
        db_cursor.execute(
            "SELECT message AS text, sender AS user, created_at FROM chat_history WHERE user_email = %s AND chat_id = %s ORDER BY id ASC",
            (user_email, chat_id,)
        )
        chat_history = db_cursor.fetchall()
        db_cursor.close()
        return jsonify(chat_history), 200


@app.route('/chat/update/<int:chat_id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_chat_name(chat_id):
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', 'https://pulse-tracker.vercel.app')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        return response
    elif request.method == 'PUT':
        user_email = get_jwt_identity()
        new_chat_name = request.json.get('chat_name')
        if not new_chat_name:
            return jsonify({'error': 'Missing chat_name parameter'}), 400
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "SELECT id FROM chats WHERE id = %s AND user_email = %s",
            (chat_id, user_email,)
        )
        chat = db_cursor.fetchone()
        if not chat:
            db_cursor.close()
            return jsonify({'error': 'Chat not found or you do not have permission to update'}), 404
        db_cursor.execute(
            "UPDATE chats SET chat_name = %s WHERE id = %s",
            (new_chat_name, chat_id,)
        )
        db_connection.commit()
        db_cursor.close()
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "SELECT chat_name FROM chats WHERE id = %s",
            (chat_id,)
        )
        updated_chat_name = db_cursor.fetchone()[0]
        db_cursor.close()
        return jsonify(
            {'message': 'Chat name updated successfully', 'chat_id': chat_id, 'chat_name': updated_chat_name}), 200


@app.route('/chat/<int:chat_id>', methods=['DELETE'])
@jwt_required()
def delete_chat(chat_id):
    user_email = get_jwt_identity()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "SELECT id FROM chats WHERE id = %s AND user_email = %s",
        (chat_id, user_email,)
    )
    chat = db_cursor.fetchone()
    if not chat:
        db_cursor.close()
        return jsonify({'error': 'Chat not found or you do not have permission to delete'}), 404
    db_cursor.execute(
        "DELETE FROM chat_history WHERE chat_id = %s",
        (chat_id,)
    )
    db_cursor.execute(
        "DELETE FROM chats WHERE id = %s",
        (chat_id,)
    )
    db_connection.commit()
    db_cursor.close()
    return jsonify({'message': 'Chat and its history deleted successfully'}), 200


@app.route("/chat/message", methods=["POST"])
@jwt_required()
def save_chat_message():
    user_email = get_jwt_identity()
    message = request.json.get("message")
    sender = request.json.get("sender")
    chat_id = request.json.get("chat_id")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "SELECT COUNT(*) FROM users WHERE email = %s", (user_email,)
    )
    result = db_cursor.fetchone()
    if result[0] == 0:
        return jsonify({"error": "User email not found"}), 400
    db_cursor.execute(
        "INSERT INTO chat_history (user_email, message, sender, chat_id) VALUES (%s, %s, %s, %s)",
        (user_email, message, sender, chat_id)
    )
    db_connection.commit()
    db_cursor.close()
    return jsonify({"message": "Message saved"}), 201


@app.route("/chat/create", methods=["POST"])
@jwt_required()
def create_chat():
    user_email = get_jwt_identity()
    chat_name = request.json.get("chat_name")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT INTO chats (chat_name, user_email) VALUES (%s, %s)",
        (chat_name, user_email),
    )
    db_connection.commit()
    chat_id = db_cursor.lastrowid
    db_cursor.close()
    return jsonify({"message": "Chat created", "chat_id": chat_id}), 201


@app.route('/chat/list', methods=['GET'])
@jwt_required()
def get_chat_list():
    user_email = get_jwt_identity()
    db_cursor = db_connection.cursor(dictionary=True)
    db_cursor.execute('SELECT id, chat_name FROM chats WHERE user_email = %s', (user_email,))
    chats = db_cursor.fetchall()
    db_cursor.close()
    return jsonify(chats), 200


if __name__ == "__main__":
    app.run(debug=True)
