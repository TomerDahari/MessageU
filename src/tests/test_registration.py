import socket

HOST = "127.0.0.1"
PORT = 1357  # ודא שזה הפורט שבו השרת מאזין

def test_register(username):
    """Sends a registration request to the server and prints the response"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"\n📡 Trying to register '{username}' at {HOST}:{PORT}...")
            s.connect((HOST, PORT))
            print("✅ Connection established.")

            request = f"110 {username}"
            print(f"➡️ Sending request: {request}")

            s.sendall(request.encode())
            response = s.recv(1024).decode()

            print(f"⬅️ Response received: {response}")
            return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("\n📝 Running Registration Tests...\n")
    response1 = test_register("Alice")  # משתמש חדש
    response2 = test_register("Alice")  # ניסיון לרישום כפול - צריך להחזיר שגיאה
    response3 = test_register("Bob")    # משתמש נוסף
