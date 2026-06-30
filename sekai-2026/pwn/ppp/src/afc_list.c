/*
 * afc_list -- interactive AFC client for a connected device.
 *
 * A device speaks the com.apple.afc protocol on the connected socket; we are
 * the host and drive libimobiledevice's real AFC client. Type commands to
 * browse the device:
 *
 *     ls   <path>            list a directory
 *     info <path>            stat a path
 *     read <path>            read a file
 *     write <path> <data>    write a file
 *     mkdir <path>           create a directory
 *     rm   <path>            remove a path
 *     devinfo                device information
 *     help / quit
 *
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>

#include <libimobiledevice/libimobiledevice.h>
#include <libimobiledevice/afc.h>

/* Complete the library's opaque handle types (layouts match the linked lib). */
typedef struct {
    char     magic[8];
    uint64_t entire_length, this_length, packet_num, operation;
} AFCPacket;

struct idevice_connection_private {
    void *device;
    enum idevice_connection_type type;
    void *data;
    void *ssl_data;
    unsigned int ssl_recv_timeout;
    int status;
};
struct service_client_private {
    struct idevice_connection_private *connection;
};
struct afc_client_private {
    struct service_client_private *parent;
    AFCPacket *afc_packet;
    uint32_t packet_extra;
    pthread_mutex_t mutex;
    int free_parent;
};

#define AFC_MAGIC_STR "CFA6LPAA"

/* free the parsed list (in cleanup order: reverse) */
static void free_list(char **list, int n)
{
    for (int i = n - 1; i >= 0; i--) free(list[i]);
    free(list);
}

/* directory / device listings: one entry per line */
static void print_names(char **list)
{
    int n = 0;
    while (list[n]) { puts(list[n]); n++; }
    free_list(list, n);
}

/* stat / device info: "key: value" pairs */
static void print_kv(char **list)
{
    int n = 0;
    while (list[n]) n++;
    for (int i = 0; i + 1 < n; i += 2)
        printf("%s: %s\n", list[i], list[i + 1]);
    free_list(list, n);
}

/* read one command line (up to '\n') from fd; returns length or -1 on EOF */
static int read_line(int fd, char *out, int max)
{
    char tmp[256];
    int n = 0;
    for (;;) {
        char c;
        ssize_t r = read(fd, &c, 1);
        if (r <= 0) return n ? n : -1;
        if (c == '\n') break;
        if (c == '\r') continue;
        tmp[n++] = c;
    }
    tmp[n] = '\0';
    if (n > max - 1) n = max - 1;
    memcpy(out, tmp, n);
    out[n] = '\0';
    return n;
}

int main(int argc, char **argv)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    int fd = 0;  /* device socket (socat dups it to stdin/stdout) */

    struct idevice_connection_private conn;
    memset(&conn, 0, sizeof(conn));
    conn.type = CONNECTION_NETWORK;
    conn.data = (void *)(intptr_t)fd;

    struct service_client_private svc;
    svc.connection = &conn;

    struct afc_client_private *afcp = calloc(1, sizeof(*afcp));
    afcp->parent = &svc;
    afcp->packet_extra = 1024;
    afcp->afc_packet = (AFCPacket *)calloc(1, sizeof(AFCPacket) + afcp->packet_extra);
    memcpy(afcp->afc_packet->magic, AFC_MAGIC_STR, 8);
    afcp->afc_packet->packet_num = 0;
    pthread_mutex_init(&afcp->mutex, NULL);
    afcp->free_parent = 0;
    afc_client_t afc = (afc_client_t)afcp;

    puts("Apple File Conduit client -- device connected.");
    puts("Type 'help' for commands.");

    char line[512];
    for (;;) {
        printf("afc> ");
        if (read_line(fd, line, sizeof(line)) < 0) break;

        char *cmd = strtok(line, " ");
        if (!cmd) continue;
        char *arg = strtok(NULL, " ");
        char *arg2 = strtok(NULL, "");

        if (!strcmp(cmd, "quit") || !strcmp(cmd, "exit")) {
            break;
        } else if (!strcmp(cmd, "help")) {
            puts("commands: ls <path> | info <path> | read <path> |"
                 " write <path> <data> | mkdir <path> | rm <path> | devinfo | quit");
        } else if (!strcmp(cmd, "ls")) {
            char **l = NULL;
            afc_error_t e = afc_read_directory(afc, arg ? arg : "/", &l);
            if (e == AFC_E_SUCCESS && l) print_names(l);
            else printf("ls: afc error %d\n", e);
        } else if (!strcmp(cmd, "info")) {
            char **l = NULL;
            afc_error_t e = afc_get_file_info(afc, arg ? arg : "/", &l);
            if (e == AFC_E_SUCCESS && l) print_kv(l);
            else printf("info: afc error %d\n", e);
        } else if (!strcmp(cmd, "devinfo")) {
            char **l = NULL;
            afc_error_t e = afc_get_device_info(afc, &l);
            if (e == AFC_E_SUCCESS && l) print_kv(l);
            else printf("devinfo: afc error %d\n", e);
        } else if (!strcmp(cmd, "read")) {
            uint64_t h = 0;
            afc_error_t e = afc_file_open(afc, arg ? arg : "/", AFC_FOPEN_RDONLY, &h);
            if (e != AFC_E_SUCCESS) { printf("read: open failed (%d)\n", e); continue; }
            char data[0x800];
            uint32_t got = 0;
            e = afc_file_read(afc, h, data, sizeof(data), &got);
            afc_file_close(afc, h);
            if (e == AFC_E_SUCCESS) { fwrite(data, 1, got, stdout); putchar('\n'); }
            else printf("read: failed (%d)\n", e);
        } else if (!strcmp(cmd, "write")) {
            uint64_t h = 0;
            afc_error_t e = afc_file_open(afc, arg ? arg : "/", AFC_FOPEN_WRONLY, &h);
            if (e != AFC_E_SUCCESS) { printf("write: open failed (%d)\n", e); continue; }
            uint32_t wrote = 0;
            const char *d = arg2 ? arg2 : "";
            afc_file_write(afc, h, d, (uint32_t)strlen(d), &wrote);
            afc_file_close(afc, h);
            printf("wrote %u bytes\n", wrote);
        } else if (!strcmp(cmd, "mkdir")) {
            afc_error_t e = afc_make_directory(afc, arg ? arg : "/");
            puts(e == AFC_E_SUCCESS ? "OK" : "mkdir failed");
        } else if (!strcmp(cmd, "rm")) {
            afc_error_t e = afc_remove_path(afc, arg ? arg : "/");
            puts(e == AFC_E_SUCCESS ? "OK" : "rm failed");
        } else {
            puts("unknown command (try 'help')");
        }
    }
    return 0;
}
