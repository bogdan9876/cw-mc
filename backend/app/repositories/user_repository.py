from app.database import get_db_connection


def get_user_by_email(email):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user


def create_user(username, email, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, password)
    )
    connection.commit()
    cursor.close()
    return {"message": "Registration successful"}


def update_user_profile(email, name, surname, phone_number, address):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET name = %s, surname = %s, phone_number = %s, address = %s WHERE email = %s",
        (name, surname, phone_number, address, email)
    )
    connection.commit()
    cursor.close()
    return {"message": "User data updated successfully"}
