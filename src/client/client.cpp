#include <iostream>
#include "client_handler.h"

void printMenu() {
    std::cout << "\nMessageU client v1 at your service.\n\n"
              << "110) Register\n"
              << "120) Request for clients list\n"
              << "130) Request for public key\n"
              << "140) Request for waiting messages\n"
              << "150) Send a text message (encrypted)\n"
              << "151) Send a request for symmetric key\n"
              << "152) Send your symmetric key\n"
              << " 0) Exit client\n"
              << "? ";
}

int main() {
    std::string choice;

    while (true) {
        printMenu();
        std::getline(std::cin, choice);

        if (choice == "0") {
            std::cout << "Exiting client.\n";
            break;
        }

        handleClientChoice(choice); // קריאה לפונקציה שמטפלת בבחירה
    }

    return 0;
}
