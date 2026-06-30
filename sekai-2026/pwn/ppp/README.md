# Writeup: ppp (SekaiCTF 2026)

- **Event:** [SekaiCTF 2026](https://ctf.sekai.team) ([CTFTime](https://ctftime.org/event/3113/))
- **Challenge:** ppp
- **Category:** pwn
- **Solved by:** [dopri](https://github.com/DoPri/)
- **Remote:** `ppp.chals.sekai.team:1337`

This was a 0-day challenge. The vulnerability is a real, previously unknown bug in [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice) (8k stars on GitHub), a open-source library for communicating with iOS devices over the AFC (Apple File Conduit) protocol.
The challenge binary (`afc_list`) is a thin, "safe" wrapper around the real library. Ehe exploitable bug lives in libimobiledevice's own `afc_receive_data()` function, not in challenge-specific code.

The Dockerfile pins specific commits of the libimobiledevice stack:

| Library               | Commit                                     |
| --------------------- | ------------------------------------------ |
| libplist              | `32428abacb909988e8e960a8845a6430b17b6a60` |
| libimobiledevice-glue | `da770a7687f35fbb981db4d7b47b1b032cd5c2c7` |
| libusbmuxd            | `93eb168bf6b07472d17781328c21df0c60300524` |
| libtatsu              | `60a39f36d719344360ec2e87563ed43f61f0530f` |
| libimobiledevice      | `fa0f79190142bc309307967c058f89c1b36eb6b8` |

The binary is linked against glibc 2.31 on Ubuntu 20.04, compiled with `-O0 -fstack-protector-all -no-pie`, and presents an interactive `afc>` prompt with commands like `devinfo` and `read`.
A SUID `/readflag` binary on the remote prints the flag when invoked as `/readflag sekai ppp`.

## Binary Security

```
Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
SHSTK:      Enabled
IBT:        Enabled
Stripped:   No
```

## Initial Analysis

The AFC protocol uses a 0x28-byte header containing a magic (`CFA6LPAA`), `entire_length`, `this_length`, a packet number, and an operation code. The bug is in libimobiledevice's `afc_receive_data()`: it allocates a receive buffer with `malloc(entire_length - 0x28)` and then reads `this_length - 0x28` bytes into it. The two length fields are independently attacker-controlled and the function does not verify that `this_length <= entire_length`.
When `entire_length` is set to exactly `0x28`, the allocation becomes `malloc(0)`, which returns a minimal 0x20-sized tcache chunk. If `this_length` then exceeds `0x28`, the subsequent `recv` writes `this_length - 0x28` bytes into this undersized buffer, producing a heap overflow of arbitrary length.

The `devinfo` command parses the received data as a sequence of null-terminated key-value string pairs. Internally it calls `strdup` on each string and later `free`s the copies. This gives precise control over the number and size of heap allocations from the 0x20 tcache bin.

The `read` command opens a file handle, reads data via `afc_receive_data()`, then closes the handle. Each step exchanges AFC packets with the client, so we control the overflow trigger by responding with a crafted `this_length` in the data packet.

The nsjail configuration sets `persona_addr_no_randomize: true`, which disables ASLR inside the sandbox. All addresses are therefore deterministic, though the exact libc base differs a bit between local and remote environments.
Since ASLR is disabled but the exact libc base varies between environments, the exploit brute-forces a 2 MiB range around the expected base in 0x1000 steps until it finds the correct offset.

## Solution

The exploit in `solve.py` performs a GOT overwrite via tcache poisoning:

1. **Heap shaping.** Send 10 `devinfo` requests, each with two 8-byte null-terminated strings. Each devinfo allocates and frees several 0x20-sized chunks through `strdup`/`free`, populating the 0x20 tcache free list with a chain of chunks at known addresses.

2. **Heap overflow.** Issue a `read /x` command and respond to the file-read AFC packet with `entire_length = 0x28` (triggering `malloc(0)`) and `this_length = 0x28 + overflow_size`. The overflow payload writes 0x10 bytes of padding, then preserves the adjacent chunk's size field (`0x21`) and overwrites its `fd` pointer with `free@GOT` (`0x404070`). After this chunk is freed back to tcache, the chain becomes: `chunk_A -> chunk_B -> free@GOT`.

3. **GOT overwrite.** Send a final `devinfo` with multiple null-terminated strings. The internal `strdup` calls allocate from the poisoned 0x20 tcache. After `chunk_A` and `chunk_B`, the third allocation returns `free@GOT`. The `strdup` writes the string's content there, which we previously set to `system@GOT`.

4. **Command execution.** One of the other strings in the same devinfo payload is `"/readflag sekai ppp"`. When the devinfo handler later frees this string, `free("/readflag sekai ppp")` dispatches through the overwritten GOT entry and calls `system("/readflag sekai ppp")`, which prints the flag.
