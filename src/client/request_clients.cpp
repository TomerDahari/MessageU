#include "request_clients.h"
#include "network_utils.h"  // ✅ נשתמש בפונקציה מכאן
#include <iostream>

void requestClientsList() {
    std::string response = sendRequest("120");  // ✅ שימוש בפונקציה מהקובץ הנכון

    if (response == "server responded with an error") {
        std::cout << response << std::endl;
    } else if (response == "No clients registered.") {
        std::cout << "No clients found in the system.\n";
    } else {
        std::cout << "Registered clients: " << response << std::endl;
    }
}
