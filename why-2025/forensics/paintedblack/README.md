# Writeup: Painted Black (WHY2025 CTF)

**Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
**Challenge:** Painted Black
**Category:** Forensics
**Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a macro-enabled Word document `case-2025-0412-public.docm`.

## Initial Analysis

The `.docm` extension indicates the presence of VBA macros. Using `olevba` (from `oletools`), I could extract the macro code. The macros contain an obfuscated string and a decryption routine.

My analysis of the macro (and my `decrypt.py` reconstruction) revealed a simple XOR encryption scheme. The decryption key is derived from a "username".

```python
def decrypt_vba_text(encrypted_text: str, username: str) -> str:
    key = username.lower().replace(" ", "")
    # ...
    decrypted_char_code = ord(char) ^ ord(key_char) ^ 0x7B
    # ...
```

The encryption also involves an additional XOR with `0x7B`.

## Solution

The challenge requires identifying the correct username to generate the key. This information is typically found within the document's metadata (Author, Last Modified By).

My metadata analysis of `case-2025-0412-public.docm` (using `exiftool`) revealed the author/user: **Olivia Renshaw**.

My `decrypt.py` script confirms this, as it attempts to brute-force the username but also includes a hardcoded successful call:

```python
print(decrypt_vba_text(encrypted_content, "Olivia Renshaw".replace(" ", "").lower()))
```

Using "Olivia Renshaw" as the username, I successfully decrypted the hardcoded ciphertext string, revealing the flag.
