#include "client_handler.h"
#include "register.h"
#include "request_clients.h"
#include "request_public_key.h"
#include "request_messages.h"
#include "send_message.h"  // ✅ נוספה התמיכה בבקשות 150, 151, 152
#include "network_utils.h"
#include <iostream>

void handleClientChoice(const std::string& choice) {
    if (choice == "110") { 
        registerUser();
    } else if (choice == "120") { 
        requestClientsList();
    } else if (choice == "130") { 
        requestPublicKey();
    } else if (choice == "140") { 
        requestWaitingMessages();
    } else if (choice == "150") { 
        sendEncryptedMessage();  // ✅ בקשה 150
    } else if (choice == "151") { 
        requestSymmetricKey();   // ✅ בקשה 151
    } else if (choice == "152") { 
        sendSymmetricKey();      // ✅ בקשה 152
    } else {
        std::cout << "Invalid choice, try again.\n";
    }
}
