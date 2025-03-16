import subprocess
import time

# רשימת הבדיקות להרצה
tests = [
    "python -m src.tests.test_registration",
    "python -m src.tests.test_get_clients",
    "python -m src.tests.test_get_public_key",
    "python -m src.tests.test_request_symmetric_key",
    "python -m src.tests.test_send_symmetric_key",
    "python -m src.tests.test_send_message",
    "python -m src.tests.test_get_pending_messages"
]

print("\n🚀 Starting test execution...\n")

for test in tests:
    print(f"\n🔍 Running: {test}")
    process = subprocess.run(test, shell=True)
    
    if process.returncode != 0:
        print(f"❌ Test failed: {test}")
        break  # עוצר את ההרצה אם בדיקה נכשלת
    
    print(f"✅ Completed: {test}")
    time.sleep(2)  # השהיה של 2 שניות בין בדיקות

print("\n🎯 All tests completed!\n")
