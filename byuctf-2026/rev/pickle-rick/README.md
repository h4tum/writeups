# Writeup: pickle-rick (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** pickle-rick
- **Category:** Reverse Engineering
- **Solved by:** [dopri](https://github.com/DoPri/)

We receive `binary` (a stripped static ELF), `pickled.txt` (a large text file), and no other hints about the encoding.

## Initial Analysis

`pickled.txt` consists of roughly 68,000 space-separated tokens, each either `rick` or `pickle`. The filename and token names suggest a binary encoding, but the challenge does not document the mapping or any post-processing.

Treating `rick` as `1` and `pickle` as `0` produces a bit string. Grouping bits into bytes and XORing each byte with `0x98` yields binary data. Writing that out produces `unpickled`, which `file` identifies as a 64-bit ELF executable (also stripped and statically linked).

There were no challenge hints pointing at this scheme; finding it required guessing a plausible bit mapping and checking whether the output looked like structured data.

## Solution

`exploit.py` implements the decoder:

1. Read `pickled.txt` and split on whitespace.
2. Map `rick` -> `'1'`, `pickle` -> `'0'`.
3. Pack bits into bytes (8 bits per byte, skip incomplete trailing groups).
4. XOR each byte with `0x98`.
5. Write the result to `unpickled`.

After decoding, the flag is visible in the recovered ELF without executing it:

```bash
strings unpickled
```
