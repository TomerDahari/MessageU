import socket

HOST = "127.0.0.1"
PORT = 1357  

def test_get_public_key(username):
    """Sends a request to fetch a public key"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"\n📡 Requesting public key for '{username}' from {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("✅ Connection established.")

            request = f"130 {username}"
            print(f"➡️ Sending request: {request}")

            s.sendall(request.encode())
            response = s.recv(1024).decode()

            print(f"⬅️ Response received: {response}\n")
            return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("\n🔍 Running Public Key Retrieval Tests...\n")
    response1 = test_get_public_key("Alice")  
    response2 = test_get_public_key("Bob")  
    response3 = test_get_public_key("UnknownUser")  
