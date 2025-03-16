import socket
import selectors
import signal
from server.handler import RequestHandler
from server.database import Database

DEFAULT_PORT = 1357

class MessageUServer:
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.db = Database()  # Use the database
        self.handler = RequestHandler(self.db)
        self.running = True
        print(f"Using port: {DEFAULT_PORT}")

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", DEFAULT_PORT))
        server_socket.listen()
        server_socket.settimeout(1)
        print(f"Server started on port {DEFAULT_PORT}")

        signal.signal(signal.SIGINT, self.shutdown)

        try:
            while self.running:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"New connection from {addr}")

                    data = client_socket.recv(1024).decode().strip()
                    if not data:
                        print("Received empty request, closing connection.")
                        client_socket.close()
                        continue

                    print(f"Received request: {data}")  # Debugging: Show received request

                    response = self.handler.handle_request(data)
                    print(f"Response sent: {response}")  # Debugging: Show response

                    client_socket.send(response.encode())
                    client_socket.close()
                except socket.timeout:
                    pass
        finally:
            server_socket.close()
            self.db.close()
            print("Server stopped.")

    def shutdown(self, signum, frame):
        """Handles Ctrl+C to shut down the server properly"""
        print("\nShutting down server gracefully...")
        self.running = False


if __name__ == "__main__":
    server = MessageUServer()
    server.start()
