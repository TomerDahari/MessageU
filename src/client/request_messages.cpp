#include "request_messages.h"
#include "network_utils.h"
#include "utils.h"
#include <iostream>
#include <map>
#include <sstream>

std::map<std::string, std::string> symmetricKeys;  // ✅ משתנה לשמירת מפתחות סימטריים

void requestWaitingMessages() {
    std::string userId = getUserID();  // ✅ שליפת ה-UUID מתוך `me.info`
    if (userId.empty()) {
        std::cout << "Error: No user ID found. Please register first.\n";
        return;
    }

    std::string request = "140 " + userId;
    std::string response = sendRequest(request);

    if (response == "server responded with an error") {
        std::cout << response << std::endl;
        return;
    } else if (response == "No messages.") {
        std::cout << "No pending messages.\n";
        return;
    }

    std::cout << "Pending messages:\n";

    std::istringstream stream(response);
    std::string line, sender, content;
    while (std::getline(stream, line)) {
        if (line.rfind("From: ", 0) == 0) {
            sender = line.substr(6);  // שליפת שם השולח
        } else if (line.rfind("Content:", 0) == 0) {
            content = line.substr(8);  // שליפת תוכן ההודעה
        } else if (line == "-----<EOM>-----") {
            // ✅ עיבוד סוגי ההודעות:
            if (content == "Request for symmetric key") {
                std::cout << "From: " << sender << "\nContent:\n" << content << "\n-----<EOM>-----\n";
            } else if (content.rfind("Symmetric key received: ", 0) == 0) {
                std::string key = content.substr(25);
                symmetricKeys[sender] = key;
                std::cout << "From: " << sender << "\nContent:\nSymmetric key received\n-----<EOM>-----\n";
            } else {
                // ✅ ניסיון לפענוח ההודעה
                if (symmetricKeys.find(sender) != symmetricKeys.end()) {
                    std::cout << "From: " << sender << "\nContent:\n" << content << "\n-----<EOM>-----\n";
                } else {
                    std::cout << "From: " << sender << "\nContent:\nCan't decrypt message\n-----<EOM>-----\n";
                }
            }
        }
    }
}
