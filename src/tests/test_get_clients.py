import socket

HOST = "127.0.0.1"
PORT = 1357  # Make sure this matches the server's port

def test_get_clients():
    """Sends request 120 to get a list of registered clients"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Trying to connect to {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("Connection established.")
            s.sendall("120".encode())
            response = s.recv(1024).decode()
            print(f"Sent: 120 | Received: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_get_clients()
