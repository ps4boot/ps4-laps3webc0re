#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>

#define MAGIC 0x0000EA6E
#define CHUNK_SIZE 4096
#define RETRY_INTERVAL 5 // Sekunden

void send_file(const char* ip, int port, const char* filepath) {
    struct stat st;
    if (stat(filepath, &st) != 0) {
        perror("stat");
        return;
    }

    while (1) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) { perror("socket"); return; }

        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        inet_pton(AF_INET, ip, &addr.sin_addr);

        if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            perror("connect");
            close(sock);
            printf("Port %d nicht erreichbar, warte %d Sekunden...\n", port, RETRY_INTERVAL);
            sleep(RETRY_INTERVAL);
            continue;
        }

        // Magic senden
        uint32_t magic_le = htole32(MAGIC);
        send(sock, &magic_le, sizeof(magic_le), 0);

        // Dateigröße senden
        uint64_t filesize_le = htole64(st.st_size);
        send(sock, &filesize_le, sizeof(filesize_le), 0);

        // Datei senden
        int fd = open(filepath, O_RDONLY);
        if (fd < 0) { perror("open"); close(sock); return; }

        uint8_t buffer[CHUNK_SIZE];
        ssize_t read_bytes;
        while ((read_bytes = read(fd, buffer, CHUNK_SIZE)) > 0) {
            send(sock, buffer, read_bytes, 0);
        }

        close(fd);
        close(sock);
        printf("Datei erfolgreich gesendet. Warte %d Sekunden...\n", RETRY_INTERVAL);
        sleep(RETRY_INTERVAL);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printf("Usage: %s <IP> <Port> <File>\n", argv[0]);
        return 1;
    }

    const char* ip = argv[1];
    int port = atoi(argv[2]);
    const char* file = argv[3];

    send_file(ip, port, file);
    return 0;
}
