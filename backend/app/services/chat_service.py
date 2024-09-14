from app.repositories.chat_repository import save_chat_message, get_chat_history


def add_chat_message(user_email, message, sender):
    return save_chat_message(user_email, message, sender)


def get_user_chat_history(user_email):
    return get_chat_history(user_email)
