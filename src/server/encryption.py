import os
import base64

def xor_encrypt(text, key):
    """Encrypts a message using XOR encryption with a binary key."""
    
    if isinstance(key, bytes):  # אם `key` הוא מסוג bytes, נמיר אותו למחרוזת hex
        key = key.hex()

    encrypted_bytes = bytearray()
    key_bytes = bytes.fromhex(key)  # המרת המפתח מ-hex חזרה ל-bytes
    key_length = len(key_bytes)

    print(f"🔐 Original text: {text}")
    print(f"🔑 Using symmetric key (decoded): {key_bytes}")

    for i, char in enumerate(text.encode()):  # הופך את הטקסט לבינארי
        encrypted_bytes.append(char ^ key_bytes[i % key_length])

    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()
    
    print(f"🛠️ XOR Encrypted bytes: {encrypted_bytes}")
    print(f"📦 Base64 Encoded: {encrypted_base64}")
    
    return encrypted_base64  # מחזיר טקסט מוצפן ב-Base64

def xor_decrypt(encrypted_text, key):
    """Decrypts an XOR-encrypted message with the given key."""
    try:
        if isinstance(key, bytes):  # If `key` is of type bytes, we convert it to a hex string
            key = key.hex()
            
        encrypted_bytes = base64.b64decode(encrypted_text)  # Converts back to bytes
        key_bytes = bytes.fromhex(key)  # Convert key back to bytes
        key_length = len(key_bytes)

        decrypted_bytes = bytearray()
        print(f"🔓 Encrypted text received: {encrypted_text}")
        print(f"📦 Base64 Decoded: {encrypted_bytes}")
        print(f"🔑 Using symmetric key (decoded): {key_bytes}")

        for i, char in enumerate(encrypted_bytes):
            decrypted_bytes.append(char ^ key_bytes[i % key_length])

        decrypted_text = decrypted_bytes.decode()
        print(f"✅ Decrypted text: {decrypted_text}")

        return decrypted_text  # Returns the original text
    except Exception as e:
        print(f"❌ Decryption error: {e}")
        return "Error: can't decrypt message"

def generate_symmetric_key():
    """Generates a random symmetric key."""
    key = os.urandom(16).hex()  # Creates a 16-byte key and returns it as hexadecimal
    print(f"🔑 Generated symmetric key: {key}")
    return key
