# Writeup: incontinent (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** incontinent
- **Category:** pwn
- **Solved by:** [dopri](https://github.com/DoPri/)
- **Remote:** `chals.cyberjousting.com:1366`

The description states that the flag lives in the program on the remote server and suggests making it "a little more leaky." We are given `incontinent_dist`, a dynamically linked x86-64 binary (not stripped).

## Initial Analysis

The program prompts for input, reads it, and prints it back. The vulnerability is not a classic overflow into a return address. Instead, the flag buffer sits on the stack immediately after the user input buffer. The read does not append a null terminator when the buffer is filled completely.

If we send exactly 32 bytes (the size of the input buffer), the subsequent output continues past our data into the adjacent stack memory where the flag is stored, because there is no `\0` byte between the end of our input and the flag bytes.

## Binary Security

```
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
```

There is no stack canary, but we do not need to control the instruction pointer for this challenge. NX and the lack of PIE are irrelevant once we only need an information leak through the echo behavior.

## Solution

`solve.py` connects to the remote (or runs the local binary with `LOCAL`), waits for the prompt, and sends 32 bytes of padding (`b'A' * 32`). It discards the echoed padding and reads the following output, which contains the flag as the first line after the leak.

This is a one-shot solve with no ROP, no GOT overwrite, and no heap manipulation.
