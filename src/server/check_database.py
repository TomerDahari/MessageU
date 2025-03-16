import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "defensive.db")

def check_database():
    print(f"\n📌 Checking database file at: {DB_FILE}\n")  # ✅ הצגת הנתיב
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check if there are tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("❌ No tables found in the database.")
        else:
            print("📌 Tables found in the database:")
            for table in tables:
                print(f"- {table[0]}")

            # Checking the contents of the 'symmetric_keys' table (symmetric keys)
            if ('symmetric_keys',) in tables:
                print("\n🔑 Checking symmetric keys stored in database...")
                cursor.execute("SELECT * FROM symmetric_keys;")
                symmetric_keys = cursor.fetchall()
                if symmetric_keys:
                    print("✅ Symmetric keys found:")
                    for row in symmetric_keys:
                        print(f"UserID: {row[0]}, SymmetricKey: {row[1]}")
                else:
                    print("❌ No symmetric keys found.")

            # Checking the contents of the customer table
            if ('clients',) in tables:
                print("\n👥 Checking registered clients...")
                cursor.execute("SELECT ID, UserName, PublicKey FROM clients;")
                clients = cursor.fetchall()
                if clients:
                    print("✅ Clients found:")
                    for row in clients:
                        print(f"ID: {row[0]}, Username: {row[1]}, PublicKey: {row[2]}")
                else:
                    print("❌ No clients found.")

            # Checking saved messages
            if ('messages',) in tables:
                print("\n📩 Checking stored messages...")
                cursor.execute("SELECT ToClient, FromClient, Type, Content FROM messages;")
                messages = cursor.fetchall()
                if messages:
                    print("✅ Messages found:")
                    for row in messages:
                        print(f"To: {row[0]}, From: {row[1]}, Type: {row[2]}, Content: {row[3]}")
                else:
                    print("❌ No messages found.")

        conn.close()
    except sqlite3.Error as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    check_database()
