#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <stdarg.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <netinet/in.h>

// === CONFIG ===
const char *blocked_domains[] = {
    "example.com", "badsite.org", "amazon.com", "aws.com", NULL
};
#define TGDK_LOG "/data/data/com.termux/files/home/tgdk105/dominancex_intercept.log"

// === OPEN INTERCEPTOR ===
int open(const char *pathname, int flags, ...) {
    static int (*real_open)(const char *, int, ...) = NULL;
    if (!real_open) real_open = dlsym(RTLD_NEXT, "open");

    // Block pathnames matching bad domains
    for (int i = 0; blocked_domains[i] != NULL; i++) {
        if (strstr(pathname, blocked_domains[i])) {
            FILE *log = fopen(TGDK_LOG, "a");
            if (log) {
                fprintf(log, "[DOMINANCEX] BLOCKED OPEN ON: %s\n", pathname);
                fclose(log);
            }
            return -1;
        }
    }

    va_list args;
    va_start(args, flags);
    int fd;

    if (flags & O_CREAT) {
        mode_t mode = va_arg(args, mode_t);
        fd = real_open(pathname, flags, mode);
    } else {
        fd = real_open(pathname, flags);
    }

    va_end(args);
    return fd;
}

// Config defaults (these can be loaded from file or hardcoded)
const char *blocked_domains[] = { "example.com", "badsite.org", "amazon.com", "aws.com", NULL };
const int blocked_ports[] = { 23, 445, 3389, 3306, 0 };  // 0 = end marker
const char *whitelist_ips[] = { "127.0.0.1", "192.168.1.1", NULL };
const int whitelist_ports[] = { 22, 53, 443, 0 };

#define TGDK_LOG "/data/data/com.termux/files/home/tgdk105/dominancex_intercept.log"
#define QQUAP_KEY "QQUAp"

// Intercept `connect`
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
    static int (*real_connect)(int, const struct sockaddr *, socklen_t) = NULL;
    if (!real_connect)
        real_connect = dlsym(RTLD_NEXT, "connect");

    struct sockaddr_in *s = (struct sockaddr_in *)addr;
    char *ip = inet_ntoa(s->sin_addr);
    int port = ntohs(s->sin_port);

    for (int i = 0; blocked_ports[i] != 0; i++) {
        if (port == blocked_ports[i]) {
            FILE *log = fopen(TGDK_LOG, "a");
            fprintf(log, "[DOMINANCEX] BLOCKED CONNECT TO PORT: %d IP: %s\n", port, ip);
            fclose(log);
            return -1;
        }
    }

    return real_connect(sockfd, addr, addrlen);
}
