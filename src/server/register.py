from .client_record import ClientRecord

class Register:
    def __init__(self, db):
        """Initialize with the database instance"""
        self.db = db

    def execute(self, username):
        """Handles client registration request"""
        if not username:
            return "Error: Missing username."

        clients = self.db.get_clients()
        if username in clients:
            return "Error: Username already exists."

        import uuid
        client_id = str(uuid.uuid4())  # Generate unique ID
        self.db.add_client(client_id, username, "", "")  # Add to database
        return f"Success: {client_id}"
