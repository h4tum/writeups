# Dreamer
 - Category: pwn
 - Final point value: 313
 - Number of solves: 10
 - Solved by: `fkil`

### Challenge Description

It would be a shame if you could exploit this sleepy binary.

### Solution

The challenge is quite nice to us and we are given:
 - Source Code
 - A win function
 - A leak to the win function

The challenge lets us execute shellcode with the following restrictions:
 - We can arbitrarily choose the first 4 bytes of the shellcode
 - Afterwards 12 NOPs follow
 - Another 86 bytes of shellcode is generated via a custom random number generator. Luckily, we can specifiy the seed of this generator


The generator function is as follows:
```C
unsigned long STATE;
char custom_random(){
    STATE = ROTL(STATE,30) ^ ROTR(STATE,12) ^ ROTL(STATE,42) ^ ROTL(STATE,4) ^ ROTR(STATE,5);
    return STATE % 256;
}
```

It definitely is not cryptographically secure and we can easily determine a seed to generate a few more bytes of shellcode.

We computed a fitting seed for a given sequence of bytes with `z3`. The state of the number generator is 8-bytes long, so it should be possible to generate up to 8 bytes shellcode additionally. From our tests however, only 4-5 bytes were possible, depending on the chosen sequence. As such, we want to create a shellcode with only 9 bytes.

Our goal was then to somehow execute `read(0, shellcode_buffer, <bigenoughlength>)` in 9 bytes and then overwrite the buffer with arbitrary shellcode. For this, we need to do the following:
 1. Set `RAX` to 0
 2. Set `RDI` to 0
 3. Set `RSI` to the buffer
 4. Make sure `RDX` is big enough
 5. Execute syscall

To create a fitting shellcode, let's look at some useful assembly gadgets:
 - zeroing any register can be done in 2 bytes using the 32-bit register xor: `xor eax,eax`
 - a `mov r1,r2` instruction takes 3 bytes, but can be done in 2 for the first 8 registers via a combination of `push` and `pop`: `push r1; pop r1`
 - `syscall` requires two bytes

As such, we can perform steps 1-3,5 in 8 bytes if the address to the buffer is stored in any register. We looked at the values of the registers at the beginning of the shellcode and discovered that `rdi` will contain the beginning of the buffer. Thus our shellcode moved `rdi` into `rsi` before zeroing `rdi`.
Now we only have 1 byte left for correctly setting `rdx`. Unfortunately, `rdx` is used for the random number generation and will contain the seed and thus be a 64-bit value. `read()` will fail if the number is too big and thus, we need to modify `rdx`. As to jump to the shellcode a `call` instruction is used, `rsp` the top value on the stack is the return address, which can be used as a valid length. Thus, the missing piece is a `pop rdx` at the beginning of the shellcode.

Finally, our shellcode for `read` is the following:

```asm
    pop rdx;
    push rdi;
    xor edi, edi; 
    pop rsi; -- this and the following instructions are created by the random number generator
    xor eax, eax;
    syscall
```

After setting up our assembly code in the program, we just send a payload to spawn a shell and then can get the flag. 
