# Writeup: hex-to-int (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** hex-to-int
- **Category:** pwn
- **Solved by:** [dopri](https://github.com/DoPri/)
- **Remote:** `chals.cyberjousting.com:1365`

The challenge description jokes about a "vibe coded" hex converter that only implements conversions up to `0xff` and offers an "expand table" feature. We receive the `hex_to_int2` binary (not stripped).

## Initial Analysis

The program presents a menu: look up a hex digit in a conversion table, or expand the table by adding a new entry. The table is a global array of 32-bit integers. The expand path asks for a hex character (used as an array index) and the integer value to store at that index.

The index is read as a signed 32-bit value but used without bounds checking. A negative index writes before the array base in `.bss`, which sits lower in memory than the array itself.

From the exploit script and symbol layout:

- The conversion table starts at `0x404060`.
- `exit@GOT` is at `0x404028`.
- The offset is `0x404028 - 0x404060 = -0x38` bytes, which is **-14** when treating the table as an array of 4-byte integers.
- As an unsigned 32-bit input, index -14 is entered as `0xfffffff2`.
- The `win()` function is at `0x4011d4`.

Partial RELRO leaves GOT entries writable. There is no stack canary. Without PIE, `win()` and GOT addresses are fixed.

## Binary Security

```
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    RPATH:      b'/home/macen/miniconda3/envs/ctf/lib'
    Stripped:   No
```

## Solution

`solve.py` performs a GOT overwrite:

1. Choose menu option 2 (expand table).
2. Send index `fffffff2` (array index -14) so the write targets `exit@GOT`.
3. Send the decimal value `4198868`, which is `0x4011d4`, the address of `win()`.
4. Return to the menu and send an invalid choice (e.g. `3`) so the program calls `exit()`.
5. `exit()` resolves through the corrupted GOT entry and jumps to `win()` instead, giving a shell. The script then runs `cat flag.txt`.

No code execution on the stack is required; this is a straight arbitrary write into the GOT followed by triggering the hijacked import.
