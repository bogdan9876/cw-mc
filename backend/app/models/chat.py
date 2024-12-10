class ChatMessage:
    def __init__(self, id, user_email, message, sender, created_at):
        self.id = id
        self.user_email = user_email
        self.message = message
        self.sender = sender
        self.created_at = created_at
