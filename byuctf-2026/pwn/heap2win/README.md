# Writeup: heap2win (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** heap2win
- **Category:** pwn
- **Solved by:** [dopri](https://github.com/DoPri/)
- **Remote:** `chals.cyberjousting.com:1364`

The challenge ships a C++ binary and the full source in `main.cpp`. The program is a small "button factory" where you can create buttons and push them. Each button type is a subclass of `Button` with a virtual `push()` method. The goal is to get code execution; the interesting class is `WinnerButton`, which calls `system("/bin/sh")` when pushed.

## Initial Analysis

The menu lets you create a **Hype Button** or a **Custom Button**. Creating a **Winner Button** is explicitly blocked with a message telling you that you are not a winner yet. However, `main()` allocates a `WinnerButton` on the heap before the application loop starts:

```cpp
WinnerButton *but = new WinnerButton();
Application *app = new Application();
app->run();
```

That object is never added to the application's `button_list`, but its vtable still exists in the binary at a fixed address (no PIE).

`CustomButton` reads the button name with `scanf("%s", name)` into a `char name[0x10]` member. There is no length limit, so any name longer than 16 bytes overflows the heap allocation for the `CustomButton` object and corrupts whatever chunk comes next.

The application keeps `Button*` pointers in a `std::vector`. When the vector grows, it reallocates its internal pointer array and frees the old array. After creating two `HypeButton` objects, adding a third button triggers a reallocation. The next `CustomButton` allocation can land in the freed vector storage, adjacent to the second `HypeButton` on the heap. Overflowing the custom name then overwrites the second hype button's chunk metadata and vtable pointer.

## Binary Security

```
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
```

Full RELRO means we cannot overwrite GOT entries. NX rules out shellcode on the heap. Without PIE, vtable addresses and the `WinnerButton` vtable at `0x403640` are fixed. The exploit path is a vtable hijack on an object we can still call through `pushButton()`.

## Solution

The exploit in `solve.py` follows these steps:

1. Create two `HypeButton` instances so the vector reallocates and the heap layout places the upcoming `CustomButton` next to hype button #2.
2. Create a `CustomButton` and send a 32-byte name: 16 bytes of padding (fills the `name` field), 8 bytes set to `0x21` (keeps the adjacent malloc chunk header plausible), and 8 bytes pointing to `WinnerButton`'s vtable (`0x403640`).
3. Push button index 2. The program calls `push()` on what it still thinks is a `HypeButton`, but the vtable now dispatches to `WinnerButton::push()`, which runs `system("/bin/sh")`.
