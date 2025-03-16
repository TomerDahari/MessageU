class PublicKeyRequest:
    """Handles fetching a client's public key from the database"""

    def __init__(self, db):
        self.db = db

    def execute(self, username):
        """Fetches the public key of the given user"""
        public_key = self.db.get_public_key(username)
        if public_key and public_key != "Error: Public key not found.":
            return f"Success: {public_key}"
        return "Error: User has no public key."
