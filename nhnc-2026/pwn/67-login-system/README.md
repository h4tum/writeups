# Writeup: 67-login-system (No Hack No CTF 2026)

- **Event:** [No Hack No CTF 2026](https://nhnc.ic3dt3a.org/) ([CTFTime](https://ctftime.org/event/3180/))
- **Challenge:** 67-login-system
- **Category:** pwn
- **Solved by:** [dopri](https://github.com/DoPri/)

A "login system" menu binary. You can register up to four accounts, then show/update/login/delete them. Each account is a heap chunk holding a username buffer and a `FILE*`.
The challenge ships the binary, and the target loader + libc (glibc 2.43, Arch base image).

## Binary Security

```
Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX enabled
PIE:        PIE enabled
```

PIE is on, so we need a leak first. The bug is on the heap, so the missing canary does not matter. Partial RELRO allows a GOT overwrite, but glibc 2.43 has no `__malloc_hook`/`__free_hook`, and the binary is a FILE-heavy program, so FSOP via House of Apple 2 seems sensible.

## Initial Analysis

Each account is created by `register` (`sub_1343`):

```c
v2 = malloc(0x48);                               // 0x50 chunk
// zero it out ...
*((_QWORD *)v2 + 8) = fopen("/dev/null", "a");   // FILE*  @ chunk+0x40
read(0, v2, 0x40);                               // username @ chunk+0x00
qword_4060[slot] = v2;
```

The chunk layout is `username[0x40]` at offset `0x00` and a real glibc `FILE*` at offset `0x40`. The four slot pointers live in a global array `qword_4060`.

The other menu entries expose three primitives:

- `show` (`sub_141F`) does `printf(qword_4060[slot])` followed by `write(1, chunk, 0x48)`. The first call is a format-string vulnerability (the username is the format) and the second leaks the raw chunk, including the `fopen` `FILE*` at offset `0x40`.
- `update` (`sub_154E`) does `read(0, chunk, 0x200)` into a `0x50` chunk. This is a heap overflow that it lets us overwrite the chunk's own `FILE*` field at offset `0x40`.
- `login` (`sub_14D1`) does `fwrite("login\n", 1, 6, *(FILE**)(chunk+0x40))`, a FILE operation on a pointer we control. This is our final trigger.
- `delete` (`sub_15BA`) `fclose`s the FILE and frees the chunk.

### Leaks

A single `show` yields both leaks:

- Register a username of `%11$p`. When `show` runs `printf(username)`, `%11$p` prints a libc pointer; subtracting `0x27741` gives the libc base.
- The trailing `write(1, chunk, 0x48)` returns the bytes at offset `0x40`, i.e., the `fopen` `FILE*`. That pointer is `0x50` above our chunk, so `chunk = FILE* - 0x50` recovers the heap address `C`.

## Solution

glibc 2.43 keeps the `_IO_FILE` vtable-pointer check, so we cannot forge the vtable to an arbitrary function table. We use House of Apple 2 (see the [writeup by Chovid99](https://chovid99.github.io/posts/stack-the-flags-ctf-2022/)), which stays within the legitimate `_IO_wfile_jumps` table:

```
fwrite -> _IO_wfile_xsputn -> _IO_wdefault_xsputn -> _IO_WOVERFLOW
       -> _IO_wfile_overflow -> _IO_wdoallocbuf
       -> fp->_wide_data->_wide_vtable->__doallocate(fp)   == system(fp)
```

If we make `fp->_flags` the string `"  sh"`, that final call becomes `system("  sh")`.

The exploit in `solve.py` proceeds:

1. **Leak.** Register slot 0 with username `%11$p`, then `show(0)` to recover the libc base (from the format-string print) and the chunk address `C` (from the leaked `FILE*` at offset `0x40`).

2. **Forge the FILE.** Using the `0x200`-byte `update` overflow, build a fake `_IO_FILE` at chunk base `C`:
   - `_flags = "  sh"` so the eventual call is `system("  sh")`.
   - `_IO_buf_end` (`+0x40`) `= C`. This offset is exactly the program's `FILE*` field, so `login` reads it back and uses our fake FILE (`fp = C`).
   - `_lock` (`+0x88`) `= C+0xe0`, a zeroed writable region to avoid a NULL deref in the locking code.
   - `_wide_data` (`+0xa0`) `= C+0x100`, `_mode` (`+0xc0`) `= 0` (narrow orientation so `fwrite` takes the wide overflow path), and vtable (`+0xd8`) `= _IO_wfile_jumps`.
   - The fake `_IO_wide_data` at `C+0x100` has `_IO_write_base/ptr/end` and `_IO_buf_base` all `0` (forcing the overflow -> `_IO_wdoallocbuf` path), and `_wide_vtable = C-0x50` so that `_wide_vtable->__doallocate` (offset `+0x68`) resolves to `C+0x18`, where we stored `system`.

   The same `update` write also overwrites the chunk's `FILE*` field at `+0x40` with `C`, redirecting `login` to the forged structure.

3. **Trigger.** Call `login(0)`. `fwrite` walks the wide-file overflow chain and calls `system("  sh")`.

## References

- [House of Apple 2 walkthrough (Chovid99)](https://chovid99.github.io/posts/stack-the-flags-ctf-2022/)
- [roderick01 (RoderickChan)'s original writeup](https://roderickchan.github.io/zh-cn/house-of-apple-%E4%B8%80%E7%A7%8D%E6%96%B0%E7%9A%84glibc%E4%B8%ADio%E6%94%BB%E5%87%BB%E6%96%B9%E6%B3%95-2/)
