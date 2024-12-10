class User:
    def __init__(self, id, email, password, name=None, surname=None, phone_number=None, address=None, username=None):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.address = address
        self.username = username
