#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#define ROTL(X, N)  (((X) << (N)) | ((X) >> (8 * sizeof(X) - (N))))
#define ROTR(X, N)  (((X) >> (N)) | ((X) << (8 * sizeof(X) - (N))))
unsigned long STATE; 
unsigned long CURRENT;

char custom_random(){
    STATE = ROTL(STATE,30) ^ ROTR(STATE,12) ^ ROTL(STATE,42) ^ ROTL(STATE,4) ^ ROTR(STATE,5);
    return STATE % 256;
}

void* experience(long origin){
  char* ccol= mmap (0,1024, PROT_READ|PROT_WRITE|PROT_EXEC,
              MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
    size_t k = 0;
    while(k<106){
        *(ccol+k) = 0x90; //nop just in case;
        k++;
    }
    k=16;
    *((int*)ccol) = origin;
    while(k<100){
        *(ccol+k)=custom_random();
        k++;
    }
    return ccol;

}

void sleepy(void * dream){
    int (*d)(void) = (void*)dream;
    d();
}


void win(){
    execv("/bin/sh",NULL);
}

void setup(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(){
    setup();
    long seed=0;
    printf("the win is yours at %p\n", win);
    scanf("%ld",&seed); 
    STATE = seed;
    printf("what are you thinking about?");
    scanf("%ld",&seed);
    sleepy(experience(seed));
}
