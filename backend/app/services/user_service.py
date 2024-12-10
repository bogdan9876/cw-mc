from app.repositories.user_repository import get_user_by_email, create_user, update_user_profile


def get_user(email):
    return get_user_by_email(email)


def register_user(username, email, password):
    return create_user(username, email, password)


def update_profile(email, name, surname, phone_number, address):
    return update_user_profile(email, name, surname, phone_number, address)
