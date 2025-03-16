import socket

HOST = "127.0.0.1"
PORT = 1357

def send_request(request):
    """Sends a request to the server and returns the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(request.encode())
            response = s.recv(1024).decode()
            return response
    except Exception as e:
        return f"Error: {e}"

def test_send_message(to_client, from_client, message):
    """Tests sending an encrypted message after ensuring symmetric key exists."""

    print("\n🔍 Checking if symmetric key exists...")
    key_check_response = send_request(f"130 {from_client}")

    if "Error" in key_check_response:
        print(f"❌ Symmetric key not found. Requesting one...")
        send_request(f"151 {to_client} {from_client}")  # בקשת מפתח סימטרי
        
        print("⏳ Waiting for symmetric key to be sent...")
        send_request(f"152 {to_client} {from_client}")  # שליחת מפתח סימטרי
    
    print("✅ Symmetric key ready! Sending message...")
    response = send_request(f"150 {to_client} {from_client} {message}")

    print(f"📩 Sent: 150 {to_client} {from_client} {message} | Received: {response}")

if __name__ == "__main__":
    test_send_message(
        "aad05559-4c6d-4e4a-8e0a-9b20994c5c9c", 
        "60d9fb6f-5d4e-4c9e-bfc0-2f14d0c5d8a5", 
        "Hello, this is a test message."
    )
