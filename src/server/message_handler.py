from .encryption import xor_encrypt, xor_decrypt, generate_symmetric_key

class MessageHandler:
    """Handles sending and receiving messages"""

    def __init__(self, db):
        self.db = db

    def send_message(self, to_client, from_client, message):
        """Encrypts and stores a message for a recipient."""
        print(f"📩 Sending message from {from_client} to {to_client}...")  # Debugging print
        symmetric_key = self.db.get_symmetric_key(to_client)  # 🔧 חיפוש המפתח אצל הנמען

        if not symmetric_key:
            print(f"❌ Error: No symmetric key found for {to_client}")  # Debugging print
            return "Error: No symmetric key found."

        print(f"🔑 Using symmetric key for encryption: {symmetric_key}")  # Debugging print
        encrypted_message = xor_encrypt(message, symmetric_key)
        print(f"🔐 Encrypted Message (before storing): {encrypted_message}")  # Debugging print
        self.db.store_message(to_client, from_client, 150, encrypted_message)
        return "Success: Message sent."

    def request_symmetric_key(self, to_client, from_client):
        """Stores a request for a symmetric key."""
        print(f"🔑 Requesting symmetric key from {to_client} to {from_client}")  # Debugging print
        self.db.store_message(to_client, from_client, 151, "Request for symmetric key")
        return "Success: Symmetric key request sent."

    def send_symmetric_key(self, to_client, from_client):
        """Generates a symmetric key and sends it to the recipient."""
        symmetric_key = generate_symmetric_key()
        print(f"🔑 Generating symmetric key for {to_client}: {symmetric_key}")  # Debugging print
        self.db.store_symmetric_key(to_client, symmetric_key)
        self.db.store_message(to_client, from_client, 152, symmetric_key)
        return "Success: Symmetric key sent."

    def decrypt_message(self, encrypted_text, symmetric_key):
        """Decrypts a received message using XOR encryption"""
        print(f"🔓 Attempting to decrypt message: {encrypted_text}")  # Debugging print
        print(f"🗝️ Using symmetric key: {symmetric_key}")  # Debugging print

        if not symmetric_key:
            print("❌ Error: No symmetric key provided for decryption.")
            return "Error: can't decrypt message"

        decrypted_text = xor_decrypt(encrypted_text, symmetric_key)
        print(f"✅ Successfully decrypted text: {decrypted_text}")  # Debugging print
        return decrypted_text

    def get_pending_messages(self, user_id):
        """Retrieves and decrypts pending messages for the user"""
        print(f"📩 Fetching pending messages for user {user_id}")  # Debugging print
        messages = self.db.get_pending_messages(user_id)
        symmetric_key = self.db.get_symmetric_key(user_id)
        print(f"🗝️ Retrieved symmetric key for user {user_id}: {symmetric_key}")  # Debugging print

        if not messages:
            return "No new messages."

        parsed_messages = []
        for msg in messages:
            from_user, msg_type, content = msg
            print(f"📨 Processing message from {from_user}, type: {msg_type}, content: {content}")  # Debugging print

            if msg_type == 150:  # Regular text message
                if symmetric_key:
                    decrypted_msg = self.decrypt_message(content, symmetric_key)
                    parsed_messages.append(f"From: {from_user}\nContent:\n{decrypted_msg}\n-----<EOM>-----\n")
                else:
                    print(f"❌ No symmetric key available to decrypt message from {from_user}")  # Debugging print
                    parsed_messages.append(f"From: {from_user}\nContent:\nError: can't decrypt message\n-----<EOM>-----\n")

            elif msg_type == 151:  # Request for symmetric key
                print(f"🔑 Received a symmetric key request from {from_user}")  # Debugging print
                parsed_messages.append(f"From: {from_user}\nContent:\nRequest for symmetric key\n-----<EOM>-----\n")

            elif msg_type == 152:  # Received symmetric key
                print(f"🔑 Received symmetric key from {from_user}: {content}")  # Debugging print
                self.db.store_symmetric_key(user_id, content)
                parsed_messages.append(f"From: {from_user}\nContent:\nsymmetric key received\n-----<EOM>-----\n")

        return "".join(parsed_messages)
