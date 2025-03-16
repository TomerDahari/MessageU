import socket

HOST = "127.0.0.1"
PORT = 1357

def test_request_symmetric_key(to_client, from_client):
    """Requests a symmetric key from another client."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Trying to connect to {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("Connection established.")
            s.sendall(f"151 {to_client} {from_client}".encode())
            response = s.recv(1024).decode()
            print(f"Sent: 151 {to_client} {from_client} | Received: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_request_symmetric_key("aad05559-4c6d-4e4a-8e0a-9b20994c5c9c", "60d9fb6f-5d4e-4c9e-bfc0-2f14d0c5d8a5")
