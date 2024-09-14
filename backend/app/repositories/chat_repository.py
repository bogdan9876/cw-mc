from app.database import get_db_connection

def save_chat_message(user_email, message, sender):
    """
    Зберегти повідомлення чату.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_email, message, sender) VALUES (%s, %s, %s)",
        (user_email, message, sender)
    )
    connection.commit()
    cursor.close()
    return {"message": "Message saved"}

def get_chat_history(user_email):
    """
    Отримати історію чату користувача.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT message AS text, sender AS user, created_at FROM chat_history WHERE user_email = %s ORDER BY id ASC",
        (user_email,)
    )
    chat_history = cursor.fetchall()
    cursor.close()
    return chat_history
