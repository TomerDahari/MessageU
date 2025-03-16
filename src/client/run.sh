#!/bin/bash

# הדפסת הודעה
echo "Compiling the client program..."

# שינוי תיקייה לקומפילציה
cd "$(dirname "$0")" || exit

# קומפילציה
g++ client.cpp client_handler.cpp request_clients.cpp register.cpp request_public_key.cpp request_messages.cpp send_message.cpp network_utils.cpp utils.cpp -o client.exe -lws2_32

# בדיקה אם הקומפילציה הצליחה
if [ $? -eq 0 ]; then
    echo "Compilation successful. Running the client..."
    ./client.exe
else
    echo "Compilation failed. Please check for errors."
fi
