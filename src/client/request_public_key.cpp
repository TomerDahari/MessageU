#include "request_public_key.h"
#include "network_utils.h"
#include <iostream>

void requestPublicKey() {
    std::cout << "Enter username: ";
    std::string username;
    std::getline(std::cin, username);

    if (username.empty()) {
        std::cout << "Error: Username cannot be empty.\n";
        return;
    }

    std::string request = "130 " + username;
    std::string response = sendRequest(request);  // ✅ שליחת בקשה לשרת

    if (response == "server responded with an error") {
        std::cout << response << std::endl;
    } else if (response == "User not found.") {
        std::cout << "Error: The requested user does not exist.\n";
    } else {
        std::cout << "Public key for " << username << ": " << response << std::endl;
    }
}
