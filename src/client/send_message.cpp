#include "send_message.h"
#include "network_utils.h"
#include "utils.h"  // שימוש בקריאת UUID
#include <iostream>

void sendEncryptedMessage() {  // 📌 בקשה 150
    std::string senderId = getUserID();  // מזהה השולח
    if (senderId.empty()) {
        std::cout << "Error: No user ID found. Please register first.\n";
        return;
    }

    std::cout << "Enter recipient username: ";
    std::string recipient;
    std::getline(std::cin, recipient);

    std::cout << "Enter message: ";
    std::string message;
    std::getline(std::cin, message);

    std::string request = "150 " + senderId + " " + recipient + " " + message;
    std::string response = sendRequest(request);

    std::cout << "Server response: " << response << std::endl;
}

void requestSymmetricKey() {  // 📌 בקשה 151
    std::string senderId = getUserID();  // מזהה השולח
    if (senderId.empty()) {
        std::cout << "Error: No user ID found. Please register first.\n";
        return;
    }

    std::cout << "Enter recipient username: ";
    std::string recipient;
    std::getline(std::cin, recipient);

    std::string request = "151 " + senderId + " " + recipient;
    std::string response = sendRequest(request);

    std::cout << "Server response: " << response << std::endl;
}

void sendSymmetricKey() {  // 📌 בקשה 152
    std::string senderId = getUserID();  // מזהה השולח
    if (senderId.empty()) {
        std::cout << "Error: No user ID found. Please register first.\n";
        return;
    }

    std::cout << "Enter recipient username: ";
    std::string recipient;
    std::getline(std::cin, recipient);

    std::cout << "Enter symmetric key: ";
    std::string symmetricKey;
    std::getline(std::cin, symmetricKey);

    std::string request = "152 " + senderId + " " + recipient + " " + symmetricKey;
    std::string response = sendRequest(request);

    std::cout << "Server response: " << response << std::endl;
}
