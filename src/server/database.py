import sqlite3
import os
import uuid

DB_FILE = os.path.join(os.path.dirname(__file__), "defensive.db")

class Database:
    def __init__(self):
        """Initialize the database connection and create tables if they do not exist."""
        try:
            self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print(f"🔄 Connecting to database: {DB_FILE}")
            self.create_tables()
            print("✅ Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"❌ Database Connection Error: {e}")

    def create_tables(self):
        """Creates the necessary tables if they do not exist."""
        print("🔧 Ensuring all required tables exist...")

        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    ID TEXT PRIMARY KEY, 
                    UserName TEXT UNIQUE NOT NULL, 
                    PublicKey TEXT DEFAULT '', 
                    LastSeen TEXT
                )
            """)
            print("✅ Table 'clients' is ready!")

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ToClient TEXT NOT NULL, 
                    FromClient TEXT NOT NULL, 
                    Type INTEGER NOT NULL, 
                    Content BLOB NOT NULL,
                    FOREIGN KEY (ToClient) REFERENCES clients(ID),
                    FOREIGN KEY (FromClient) REFERENCES clients(ID)
                )
            """)
            print("✅ Table 'messages' is ready!")

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS symmetric_keys (
                    UserID TEXT PRIMARY KEY,
                    SymmetricKey TEXT NOT NULL,
                    FOREIGN KEY (UserID) REFERENCES clients(ID)
                )
            """)
            print("✅ Table 'symmetric_keys' is ready!")

            self.conn.commit()
            self.verify_tables()
        except sqlite3.Error as e:
            print(f"❌ Error creating tables: {e}")

    def verify_tables(self):
        """Verifies that all required tables exist after initialization."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        print("\n📌 Tables currently in the database:")
        for table in tables:
            print(f"- {table[0]}")
        print("\n✅ Table verification complete.")

    def add_client(self, client_id, username, public_key, last_seen):
        """Registers a new client in the database."""
        try:
            if not public_key or public_key.strip() == "":
                public_key = str(uuid.uuid4())  # Generate a random public key if not provided

            self.cursor.execute("""
                INSERT INTO clients (ID, UserName, PublicKey, LastSeen) 
                VALUES (?, ?, ?, ?)""",
                (client_id, username, public_key, last_seen))
            self.conn.commit()
            print(f"✅ New client added: {username} (ID: {client_id})")
            return True
        except sqlite3.IntegrityError:
            print(f"❌ Error: Username '{username}' already exists!")
            return False

    def get_clients(self):
        """Returns a list of all registered clients' usernames."""
        self.cursor.execute("SELECT UserName FROM clients")
        clients = [row[0] for row in self.cursor.fetchall()]
        print(f"👥 Registered clients: {clients}")
        return clients

    def get_public_key(self, username):
        """Fetches the public key for the given username."""
        self.cursor.execute("SELECT PublicKey FROM clients WHERE UserName = ?", (username,))
        result = self.cursor.fetchone()
        print(f"🔍 Public Key Lookup for {username} -> {result}")
        return f"Success: {result[0]}" if result and result[0] else "Error: Public key not found."

    def store_symmetric_key(self, user_id, symmetric_key):
        """Stores a symmetric key for the given user."""
        print(f"🔑 Storing symmetric key for {user_id}: {symmetric_key}")
        try:
            self.cursor.execute("""
                INSERT INTO symmetric_keys (UserID, SymmetricKey)
                VALUES (?, ?) ON CONFLICT(UserID) DO UPDATE SET SymmetricKey = ?""",
                (user_id, symmetric_key, symmetric_key))
            self.conn.commit()
            print(f"✅ Symmetric key stored successfully for {user_id}.")
        except sqlite3.Error as e:
            print(f"❌ Error storing symmetric key: {e}")

    def get_symmetric_key(self, user_id):
        """Fetches the symmetric key for a given user."""
        self.cursor.execute("SELECT SymmetricKey FROM symmetric_keys WHERE UserID = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            key = result[0]
            print(f"🔍 Symmetric Key Lookup for {user_id} -> {key}")
            return bytes.fromhex(key)  # Convert back to binary key
        return None

    def store_message(self, to_client, from_client, msg_type, content):
        """Stores a new message in the database."""
        print(f"📩 Storing message: To={to_client}, From={from_client}, Type={msg_type}, Content={content}")
        try:
            self.cursor.execute("""
                INSERT INTO messages (ToClient, FromClient, Type, Content)
                VALUES (?, ?, ?, ?)""",
                (to_client, from_client, msg_type, content))
            self.conn.commit()
            print(f"✅ Message stored successfully.")
        except sqlite3.Error as e:
            print(f"❌ Error storing message: {e}")

    def get_pending_messages(self, user_id):
        """Fetches all pending messages for a given user."""
        self.cursor.execute("""
            SELECT FromClient, Type, Content 
            FROM messages 
            WHERE ToClient = ?""", (user_id,))
        messages = self.cursor.fetchall()
        print(f"📩 Pending messages for {user_id}: {messages}")
        return messages

    def get_messages_by_type(self, user_id, msg_type):
        """Fetches messages for a user based on message type."""
        self.cursor.execute("""
            SELECT FromClient, Content 
            FROM messages 
            WHERE ToClient = ? AND Type = ?""", (user_id, msg_type))
        messages = self.cursor.fetchall()
        print(f"📩 Messages of type {msg_type} for {user_id}: {messages}")
        return messages

    def close(self):
        """Closes the database connection."""
        self.conn.close()
        print("✅ Database connection closed.")
