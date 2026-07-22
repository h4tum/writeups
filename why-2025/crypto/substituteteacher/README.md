Substitute Teacher
===
- Category: `crypto`
- Author: `dopri`

We are provided with a text file `story.txt`.

## Initial Analysis

The `story.txt` file contains what appears to be ciphertext starting with "Lcb...".

## Solution

When I inspected the first word of `story.txt`, "Lcb":

- 'L' maps to 'T' (via my script's mapping).
- 'c' maps to 'h'.
- 'b' maps to 'e'.

This decrypts to "The", confirming that the script performs a simple monoalphabetic substitution decryption.

In my `decrypt.py`, I defined two strings: `plain` and `cipher`.

```python
plain = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher = "kehmywrgupjtczqaxfnlvsodbiKEHMYWRGUPJTCZQAXFNLVSODBI"
```

The script creates a mapping from `plain` characters to `cipher` characters.

```python
decrypt_map = {plain[i]: cipher[i] for i in range(len(plain))}
```

The script reads `story.txt`, applies the substitution, and prints the result. The decrypted text is a short story that ends with the flag.
