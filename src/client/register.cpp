#include "register.h"
#include "network_utils.h"
#include <fstream>
#include <iostream>

void registerUser() {
    std::string username, request;

    std::cout << "Enter username: ";
    std::getline(std::cin, username);

    if (username.length() > 255) {
        std::cout << "Error: Username too long.\n";
        return;
    }

    // שליחת בקשת רישום לשרת
    request = "110 " + username;
    std::string response = sendRequest(request);  // ✅ שליחת הבקשה

    if (response == "server responded with an error") {
        std::cout << response << std::endl;
    } else {
        // ✅ שמירת שם המשתמש + UUID **רק** ב- `me.info`
        std::ofstream infoFile("me.info");
        infoFile << "Username: " << username << std::endl;
        infoFile << "UUID: " << response << std::endl;
        infoFile.close();

        std::cout << "Registration successful. Your ID: " << response << std::endl;
        std::cout << "Your details have been saved in 'me.info'.\n";
    }
}
