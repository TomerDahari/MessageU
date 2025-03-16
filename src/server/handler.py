from .register import Register
from .message_handler import MessageHandler

class RequestHandler:
    """Handles different client requests"""

    def __init__(self, db):
        self.db = db  # שימוש בבסיס הנתונים
        self.register_handler = Register(self.db)  # מחלקת רישום
        self.message_handler = MessageHandler(self.db)  # מחלקת ניהול הודעות

    def handle_request(self, data):
        """Processes client requests"""
        parts = data.split()
        if not parts:
            return "Error: Invalid request."

        request_type = parts[0]

        if request_type == "110":  # Register request
            username = parts[1] if len(parts) > 1 else ""
            return self.register_handler.execute(username)  # Handle user registration

        if request_type == "120":  # Request for clients list
            clients = self.db.get_clients()
            return ",".join(clients) if clients else "No clients registered."

        if request_type == "130":  # Request for public key
            username = parts[1] if len(parts) > 1 else ""
            return self.db.get_public_key(username)

        if request_type == "140":  # Request for pending messages
            user_id = parts[1] if len(parts) > 1 else ""
            return self.message_handler.get_pending_messages(user_id)

        if request_type == "150":  # Send encrypted message
            return self.message_handler.send_message(parts[1], parts[2], " ".join(parts[3:]))

        if request_type == "151":  # Request symmetric key
            return self.message_handler.request_symmetric_key(parts[1], parts[2])

        if request_type == "152":  # Send symmetric key
            return self.message_handler.send_symmetric_key(parts[1], parts[2])

        return "Error: Unknown request."
