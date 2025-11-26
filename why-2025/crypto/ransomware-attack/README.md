# Writeup: Ransomware Attack (WHY2025 CTF)

**Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
**Challenge:** Ransomware Attack
**Category:** Cryptography
**Solved by:** [dopri](https://github.com/DoPri/)

We are provided with an encryption script `encrypt.py` and an encrypted file `important.txt.encrypted`.

## Initial Analysis

The `encrypt.py` script implements a custom polyalphabetic cipher that shifts characters based on a rotating counter.

```python
def encrypt_text(text):
    counter = 0
    encrypted_text = ""

    for i in range(0, len(text), 10):
        counter = (counter + 1) % 26
        encrypted_text += shift_chars(text[i:i+10], counter)
    return encrypted_text
```

The logic is as follows:

1. The text is processed in chunks of 10 characters.
2. A `counter` is incremented (modulo 26) _before_ processing each chunk.
   - 1st chunk (0-9): `counter` = 1
   - 2nd chunk (10-19): `counter` = 2
   - ...
3. Each character in the chunk is shifted forward by the current `counter` value within the alphabet `a-z`. Non-alphabet characters are left unchanged.

## Solution

To decrypt the file, I simply needed to reverse this process. I iterated through the ciphertext in chunks of 10, calculating the same `counter` value for each step, but subtracting the counter instead of adding it.

My `decrypt.py` implements exactly this logic:

```python
def decrypt_text(text):
    counter = 0
    decrypted_text = ""

    for i in range(0, len(text), 10):
        counter = (counter + 1) % 26
        decrypted_text += shift_chars_back(text[i : i + 10], counter)
    return decrypted_text
```

Executing `./decrypt.py important.txt.encrypted` produced `important.txt.decrypted`, which contains the flag.
