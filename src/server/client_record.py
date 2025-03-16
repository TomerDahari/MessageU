import uuid

class ClientRecord:
    def __init__(self, username):
        self.username = username
        self.client_id = str(uuid.uuid4())  # Generate unique client ID

    def to_dict(self):
        """Convert client data to a dictionary format"""
        return {"username": self.username, "client_id": self.client_id}
