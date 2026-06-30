# Writeup: intro-2 (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** intro-2
- **Category:** pwn
- **Solved by:** [dopri](https://github.com/DoPri/)
- **Remote:** `chals.cyberjousting.com:1367`

The note in `info.txt` mentions that `byuctf{welcome_to_rev_fellas}` belonged to a separate "intro 1" challenge. Intro 2 itself is solved by exploiting the remote `intro` binary. The service runs inside `pwn.red/jail` (60 second time limit, 20 MB memory, per the `Dockerfile`).

The program gives you two attempts to "guess the flag." Each attempt reads a line and passes it to `printf` with the user string as the format string, which is a classic format string vulnerability.

## Initial Analysis

On the first attempt we can use the format string to read values from the stack. The exploit uses `%39$p` to leak a return address that points into the main binary. Subtracting the fixed offset `0x5c9` from that leak yields the PIE base. From the base we compute:

- `win()` at `base + 0x53c`
- `puts@GOT` at `base + 0x3018`

On the second attempt we overwrite `puts@GOT` with the address of `win()` using pwntools `fmtstr_payload`. The format string argument offset is 20. Short writes are used to keep the payload under the input size limit (the script checks that the payload is at most 99 bytes).

Because the binary is PIE-enabled and ASLR is in play, the absolute addresses of `puts@GOT` and `win()` change each run. Some bases produce addresses containing whitespace bytes (`0x09`, `0x0a`, `0x0b`, `0x0c`, `0x0d`, `0x20`), which break the format string write or the payload construction. The script loops until a favorable base appears.

After the overwrite, any call to `puts()` (for example when printing an error message) transfers control to `win()`, which spawns a shell.

## Binary Security

```
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
```

Partial RELRO allows GOT overwrites. PIE means we must leak before we write. There is still no stack canary, which keeps format string exploitation straightforward once the correct stack offset is known.

## Solution

`solve.py` implements the two-stage attack:

1. **Leak:** Send `%39$p` on attempt 1, parse the leaked pointer, derive `exe_base`, `win_addr`, and `puts_got`. Abort and reconnect if the GOT address contains whitespace.
2. **Write:** Build `fmtstr_payload(20, {puts_got: win_addr}, write_size='short', badbytes=...)` and send it on attempt 2.
3. **Shell:** Send `cat flag.txt; exit` and scan the output for the `byuctf{...}` wrapper.

The outer `while not solve(): pass` loop handles ASLR retries on the remote service.
