#include "network_utils.h"
#include <winsock2.h>
#include <iostream>

#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 1357

std::string sendRequest(const std::string& request) {
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server_addr;
    char buffer[4096] = {0};

    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) {
        return "Error: Winsock initialization failed.";
    }

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        WSACleanup();
        return "Error: Socket creation failed.";
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        closesocket(sock);
        WSACleanup();
        return "Error: Connection to server failed.";
    }

    send(sock, request.c_str(), request.length(), 0);
    
    int valread = recv(sock, buffer, sizeof(buffer) - 1, 0);
    closesocket(sock);
    WSACleanup();

    if (valread > 0) {
        return std::string(buffer, valread);
    } else {
        return "Error: No response from server.";
    }
}
