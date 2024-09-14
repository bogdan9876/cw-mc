from app.database import get_db_connection

def save_heart_rate(user_email, heart_rate):
    """
    Записати дані серцебиття.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO health_data (heart_rate, user_email) VALUES (%s, %s)",
        (heart_rate, user_email)
    )
    connection.commit()
    cursor.close()
    return {"message": "Data saved successfully"}

def get_recent_heart_rate(user_email, limit=10):
    """
    Отримати останні дані серцебиття.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT heart_rate, created_at FROM health_data WHERE user_email = %s ORDER BY id DESC LIMIT %s",
        (user_email, limit)
    )
    data = cursor.fetchall()
    cursor.close()
    return data
