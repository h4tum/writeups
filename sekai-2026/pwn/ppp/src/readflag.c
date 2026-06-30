#include <stdio.h>
#include <string.h>

#ifndef FLAG
#define FLAG "SEKAI{REPLACE_ME}"
#endif

int main(int argc, char **argv)
{
    if (argc != 3 || strcmp(argv[1], "sekai") != 0 || strcmp(argv[2], "ppp") != 0) {
        fprintf(stderr, "usage: %s sekai ppp\n", argv[0]);
        return 1;
    }

    puts(FLAG);
    return 0;
}
