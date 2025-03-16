#include "utils.h"
#include <fstream>
#include <iostream>

std::string getUserID() {
    std::ifstream infoFile("me.info");
    std::string line, userId;

    if (infoFile.is_open()) {
        while (std::getline(infoFile, line)) {
            if (line.rfind("UUID: ", 0) == 0) {  // חיפוש שורה שמתחילה ב- "UUID: "
                userId = line.substr(6);  // חותך את "UUID: " ומחזיר את הערך
                break;
            }
        }
        infoFile.close();
    } else {
        std::cerr << "Error: Unable to open me.info. Have you registered?\n";
        return "";
    }

    return userId;
}
