import socket
import sqlite3
import os
from src.server.encryption import xor_decrypt


HOST = "127.0.0.1"
PORT = 1357
DB_FILE = os.path.join(os.path.dirname(__file__), "../server/defensive.db")

def fetch_symmetric_key(user_id):
    """Fetch the symmetric key from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT SymmetricKey FROM symmetric_keys WHERE UserID = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def fetch_pending_messages(user_id):
    """Fetch all pending messages for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT FromClient, Type, Content FROM messages WHERE ToClient = ?", (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def test_message_decryption(user_id):
    """Retrieve messages, fetch the symmetric key, and attempt decryption."""
    symmetric_key = fetch_symmetric_key(user_id)
    messages = fetch_pending_messages(user_id)
    print(f"\n🔑 Symmetric Key for {user_id}: {symmetric_key}")
    
    if not messages:
        print("📭 No messages found.")
        return
    
    for from_user, msg_type, content in messages:
        print(f"\n📨 Message from {from_user}, Type: {msg_type}")
        if msg_type == 150:
            if symmetric_key:
                decrypted_msg = xor_decrypt(content, symmetric_key)
                print(f"🔓 Decrypted message: {decrypted_msg}")
            else:
                print("❌ No symmetric key found for decryption.")
        else:
            print(f"🔹 Non-text message type {msg_type}, Content: {content}")

def test_get_pending_messages(user_id):
    """Send a request to the server to fetch messages."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"\n📡 Connecting to {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            request = f"140 {user_id}"
            s.sendall(request.encode())
            response = s.recv(4096).decode()
            print(f"\n⬅️ Server Response:\n{response}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    alice_id = "aad05559-4c6d-4e4a-8e0a-9b20994c5c9c"
    print("\n🔍 Testing message retrieval and decryption...")
    test_message_decryption(alice_id)
    print("\n📡 Testing server request...")
    test_get_pending_messages(alice_id)
